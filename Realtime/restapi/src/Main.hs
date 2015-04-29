{-# LANGUAGE OverloadedStrings #-}
module Main where

import Control.Monad (forever, mzero, liftM)
import Data.Aeson
import Data.Foldable (mapM_,forM_,foldl)
import Data.Maybe
import Data.Monoid
import Data.Sequence (Seq)
import Data.Text (Text, toLower, isInfixOf)
import qualified Data.Map as Map
import Network.Socket hiding (recv)
import Network.Socket.ByteString (recv)
import System.IO
import System.Process
import Text.Printf

import qualified Data.ByteString as BS
import qualified Data.ByteString.Char8 as BC
import qualified Data.ByteString.Lazy as BL
import qualified Data.Sequence as Seq
import qualified Data.Text.IO as TIO

import Data.UnixTime
import Control.Concurrent.MVar
import Control.Concurrent
import Control.Monad.IO.Class

import Snap.Core
import Snap.Http.Server

data Tweet = Tweet {
    text :: Text,
    sentiment :: Bool -- true == pos
}

instance FromJSON Tweet where
    parseJSON (Object v) = Tweet <$> v .: "text" <*>
                            ((==("pos"::String)) <$> (v.:"sentiment"))
    parseJSON _ = mzero

untilM :: IO a -> (a -> IO Bool) -> IO a
untilM action fun = do
    res <- action
    bool <- fun res
    if bool then return res else untilM action fun

getCompany :: Text -> Maybe Text
getCompany text' = 
    let lower = toLower text'
        filtered = filter (`isInfixOf`lower)
                    ["google", "apple", "amazon", "samsung"]
    in
    if null filtered then Nothing else Just (head filtered)
        
dataService :: MVar (Seq (UnixTime, Text, Bool)) -> IO ()
dataService store = do
    sock <- socket AF_INET Datagram defaultProtocol
    addr <- SockAddrInet 5551 <$> inet_addr "127.0.0.1"
    bind sock addr

    forever $ do
        bytes <- recv sock (1024*1024)

        let tweet = decode (BL.fromChunks [bytes]) :: Maybe Tweet
        let company = getCompany =<< (text <$> tweet)
        let dat = (,) <$> company <*> (sentiment <$> tweet)
        
        forM_ dat $ \(txt, sent) -> do
            nixTime@(UnixTime mSec mMicro) <- getUnixTime
            putStrLn $ "ts " ++ (show nixTime)
            modifyMVar_ store $ \aSeq -> do
                let fst3 (a,_,_) = a
                    pastNixTime = UnixTime (mSec - 1800) mMicro
                    filtered = Seq.dropWhileL ((<pastNixTime).fst3) aSeq
                    appended = filtered Seq.|> (nixTime, txt, sent)
                    in
                    return appended

site :: MVar (Seq (UnixTime, Text, Bool)) -> Snap ()
site store =
    let aggregate :: Seq (UnixTime, Text, Bool) -> Map.Map Text (Int, Int)
        aggregate = 
            let foo (a, b) (c, d) = (a+c,b+d)
                castB True = (1, 0)
                castB False = (0, 1)
                in
            foldl (\mp (_,t,b) -> Map.insertWith foo t (castB b) mp)
                Map.empty 
        writeData = liftIO $
            (BL.toStrict . encode . aggregate) <$> readMVar store
    in
    route [("data", writeBS =<< writeData)]

main :: IO()
main = do
    store <- newMVar $ Seq.empty
    _ <- forkIO (dataService store)
    quickHttpServe (site store)
