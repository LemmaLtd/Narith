-- [Narith]
-- File: IOManager.hs
-- Author: Saad Talaat
-- Date: 17th of July 2013
-- Brief: extensible abstraction for IO

module Narith.Base.IOManager(File,IOEvent(..)) where

import System.IO
import Control.Monad
import qualified System.Directory

data File= File { fileName :: String
  , fileMode :: IOMode}

class Monad m => IOEvent f m | m -> f
  where
    createHandle :: f -> m Handle
    isValid :: f -> m Bool

instance IOEvent File IO
  where
    createHandle f = System.IO.openFile (fileName f) (fileMode f)
    isValid f = System.Directory.doesFileExist (fileName f)


