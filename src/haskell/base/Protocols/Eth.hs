-- [Narith]
-- File: Eth.hs
-- Author: Saad Talaat
-- Date: 17th of July 2013
-- Brief: Structure to hold Ethernet info

module Narith.Protocols.Eth () where
import Narith.Protocol

-- local datatype holding eth info
data EthType = EthArp | EthIP | EthNone

-- dst,src can vary from native to formatted representation
data Eth = Eth {
		 dstMac :: String,
		 srcMac :: String,
		 ethType :: EthType }

instance Protocol (Prot a) where
  initProtocol (Ethernet a) = undefined -- raise exception for now
  rawProtocol (Ethernet a) = undefined -- raise exception for now..
  formatProtocol (Ethernet a) = undefined
