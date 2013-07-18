-- [Narith]
-- File: ArgManager.hs
-- Author: Saad Talaat
-- Date: 17th of July 2013
-- Brief: extensible abstraction for IO
module Narith.Base.ArgManager() where

import System.Environment
import System.Console.GetOpt
import System.Exit

-- Options Flag type
data OptFlag = Help |
  Version |
  Input {inFile ::String} |
  Output {outFile::String}

-- Process Options Flags
data OptProc = All | OptInput | OptOutput

-- Available Options
options :: [OptDescr OptFlag]
options = [
	Option ['V'] ["version"] (NoArg Version) "show version Number",
	Option ['h'] ["help"] (NoArg Help) "show help text",
	Option ['i'] ["ifile"] (ReqArg Input "Pcap File") "input pcap file path",
	Option ['o'] ["logfile"] (ReqArg Output "Session Log") "session log output file path"
	]

-- Create typeclass for Opts wrapper functions
class Monad m => Opt o m | m -> o where
  optProcess ::o -> m ()
  optVal :: o -> m String

-- Make all opts the same disregard the argument
instance Eq OptFlag where
  (==) (Input _) (Input _) = True
  (==) (Output _) (Output _) = True

-- Define them for OptProc
instance Opt OptProc IO where
-- Let's define an optProcess for Just (All) for now
  optProcess All = do
    args <- getArgs
    let (flags,nonOpts,msgs) = getOpt RequireOrder options args
    case msgs of
      [] -> putStr ""
      m  -> exitWithErrs m
    dispatch flags
-- in case Input Needed
  optVal OptInput = do
    args <- getArgs
    let (flags,nonOpts,msgs) = getOpt RequireOrder options args
    let c = (takeWhile (/= (Input "")) flags)
    case c of 
      [] -> return ""
      x  -> return (inFile(x!!0))

-- in case Output...hmm I guess we should define an identity function..
  optVal OptOutput = do
    args <- getArgs
    let (flags,nonOpts,msgs) = getOpt RequireOrder options args
    let c = (takeWhile (/= (Output "")) flags)
    case c of
      [] -> return ""
      x  -> return (outFile(x!!0))

exitWithErrs :: [String] -> IO ()
exitWithErrs [] = exitFailure
exitWithErrs (x:xs) = putStrLn ("Error: " ++ x) >> exitWithErrs xs

-- dispatch takes Flag of Options, their arguments and stored options
--dispatch :: [OptFlag] [String] [(a,b)]  -> IO ()
dispatch [] = return ()
dispatch (x:xs) = case xs of
  [] -> return()
  _ -> (getCmd x) >> dispatch xs

getCmd :: OptFlag -> IO ()

getCmd Help = help
getCmd Version = version
getCmd _ = return ()

help = putStrLn "usage: narith [options] [flags]\n-h\t: view this output.\n-v\t: verbose mode on.\n-i\t: input file.\n-o\t: output file.\n\n\tBy:\n\t\tSaad Talaat<saadtalaat@gmail.com>\n\t\tMahmoud Hard<hard.man179@gmail.com>"
version = putStrLn "v0.0.1"
