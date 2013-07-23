-- [Narith]
-- File: Eth.hs
-- Author: Saad Talaat
-- Date: 17th of July 2013
-- Brief: Structure to hold Ethernet info

module Narith.Protocols.Eth () where
import Narith.Protocol
import Data.ByteString as L
import Data.ByteString.Char8 as C
import Data.List as DL
import Data.Word
-- local datatype holding eth info
data EthType = EthArp | EthIP | EthNone
  deriving (Eq)

-- dst,src can vary from native to formatted representation
data Eth = Eth {
		 dstMac :: String,
		 srcMac :: String,
		 ethType :: EthType } |
	   EthRaw{
		ethRaw :: ByteString
		}

-- Init Ethernet representation
ethInit :: L.ByteString -> Eth
ethInit raw = (Eth dst src (mapType t)) where
  dst = DL.intercalate ":" $DL.map show $L.unpack $L.take 6 raw
  src = DL.intercalate ":" $DL.map show $L.unpack $L.take 6 $snd $L.splitAt 6 raw
  t   = lookup (read (Prelude.concat $DL.map show $L.unpack $L.take 2 $snd $L.splitAt 12 raw) :: Int) ethTypes where
    ethTypes = [(0x8000,EthIP),(0x8006,EthArp)]
  mapType (Just z) = z
  mapType Nothing = EthNone

-- retrieve raw Bytestring representation
ethToRaw :: Eth -> L.ByteString
ethToRaw (Eth dst src t) = L.append d $ L.append s tp where
  d = L.pack (
    DL.map read (
      DL.map C.unpack $(C.splitWith (==':') $ C.pack dst)
    ) :: [Word8])
  s = L.pack (Prelude.map read (Prelude.map C.unpack $(C.splitWith (==':') $ C.pack src)) :: [Word8])
  tp = L.pack $mapType $lookup t ethTypes where
    ethTypes = [(EthIP,[0x80,00]),(EthArp,[0x80,06])]
    mapType (Just z) = z
    mapType Nothing = [00,00]
-- here we suppose a is a string
instance Protocol (Eth) where
  formatProtocol (EthRaw raw) = ethInit raw
  rawProtocol a = EthRaw (ethToRaw a)
