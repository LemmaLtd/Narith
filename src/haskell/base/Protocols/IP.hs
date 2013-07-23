-- [Narith]
-- File: IP.hs
-- Author: Saad Talaat
-- Date: 19th of July 2013
-- Brief: Structure to hold IP info

module Narith.Protocols.IP () where
import Narith.Protocol
import Data.ByteString as L
import Data.ByteString.Char8 as C
import Data.List as DL
import Data.Word
-- local datatype holding eth info
data IPType = TCP | UDP | IPNone

-- dst,src can vary from native to formatted representation
data IP = IP {
		 version 	:: Int,
		 headerLength 	:: Int,
		 diffService	:: Int,
		 totalLength	:: Int,
		 identification	:: Int,
		 flags		:: Int,
		 fragOffset	:: Int,
		 protType	:: IPType,
		 checksum	:: Int,
		 srcAddr	:: String,
		 dstAddr	:: String
		} |
	  IPRaw { ipRaw :: L.ByteString }
instance Protocol (IP) where
  rawProtocol (IPRaw a) = undefined -- raise exception for now..
  formatProtocol a = undefined

