-- [Narith]
-- File: Protocol.hs
-- Author: Saad Talaat
-- Date: 18th of July 2013
-- Brief: Protocols type class including 
--        all protocols constructors if defined.

module Narith.Protocol (Prot(..),Protocol(..)) where

-- define unified datatype holding all types of
-- network protocols with each value holding a
-- subtype execlusive to each protocol impleme-
-- tation and holding its data.
-- Why this design?
-- High abstraction and locality therefore more
-- reliability. Protocols growth will only lead
-- to growth of Prot datatype with each typeclass
-- instance execlusive to its module.
-- Prot (a): where a is an exclusive datatype
-- to each protocol holding its data

data Prot a = Ethernet a | IP a | Arp a | Udp a | Tcp a | Bytes a

-- Typeclass of protocols holding function to
-- protocol structures constructors and data
-- retrival functions.
class Protocol a where
	rawProtocol:: a ->  a
	formatProtocol:: a -> a 
