-- [Narith]
-- File: Eth.hs
-- Author: Saad Talaat
-- Date: 17th of July 2013
-- Brief: Structure to hold Ethernet info

module Narith.Protocols.Eth () where
import Narith.Protocol
import Data.ByteString as L
import Data.List as DL
-- local datatype holding eth info
data EthType = EthArp | EthIP | EthNone

-- dst,src can vary from native to formatted representation
data Eth = Eth {
		 dstMac :: String,
		 srcMac :: String,
		 ethType :: EthType } |
	   EthRaw{
		ethRaw :: ByteString
		}

ethInit :: L.ByteString -> Eth
ethInit raw = (Eth dst src (mapType t)) where
  dst = DL.intercalate ":" $DL.map show $L.unpack $L.take 6 raw
  src = DL.intercalate ":" $DL.map show $L.unpack $L.take 6 $snd $L.splitAt 6 raw
  t   = lookup (read (Prelude.concat $DL.map show $L.unpack $L.take 2 $snd $L.splitAt 12 raw) :: Int) ethTypes where
    ethTypes = [(8000,EthIP),(8006,EthArp)]
  mapType (Just z) = z
  mapType Nothing = EthNone

-- here we suppose a is a string
instance Protocol (Eth) where
  initProtocol (EthRaw raw) = ethInit raw
