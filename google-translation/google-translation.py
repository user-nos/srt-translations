from deep_translator import GoogleTranslator
from tqdm import tqdm
import argparse
import pysubs2
import time

# Define color codes as constants for easier use
# Used to print with colors on terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m' # Reset color

# Get arguments parsed from the terminal for the input srt file and the output srt file paths
# E.g. terminal >> python google-translation.py -i abc.srt -o qwerty.srt -l(optional) "en" -e(optional) "utf8"
def getArgumentsParsed():
    oParser = argparse.ArgumentParser(
        description="Translation script using GoogleTranslate"
    )

    oParser.add_argument(
        "--input",
        "-i",
        help = "1st positional argument (e.g. input-file.srt)"
    )

    oParser.add_argument(
        "--output",
        "-o",
        help = "2nd positional argument (e.g. output-file.srt)"
    )

    oParser.add_argument(
        "--language",
        "-l",
        default = "en",
        help = "3rd positional argument for the target language to translate the file to"
    )

    oParser.add_argument(
        "--encoding",
        "-e",
        default = "utf8",
        help = "4th positional argument for the encoding of the input file"
    )

    oArgs = oParser.parse_args()

    return oArgs.input, oArgs.output, oArgs.language ,oArgs.encoding


# Translation of the srt file
# sInputFile    --> .srt file to be translated (path)
#                   E.g. path of input test srt file --> W:\Media\Movies\qwerty.srt
# sOutputFile   --> .srt file path and name where output file will written to
# sTargetLang   --> target language to translate to
# sEncoding     --> encoding used in the input srt for pysubs2 to load the file with (utf-8 or latin-1)
def translateSrt( sInputFile, sOutputFile, sTargetLang = "en", sEncoding = "utf8" ):
    iBatchSize = 10
    # Initialize Translator object that was imported from the library "Translate"
    oTranslator = GoogleTranslator( source= "auto", target = sTargetLang )
    
    # Load input subs file
    oSubs = pysubs2.load( sInputFile, encoding = sEncoding )

    # Filter for lines that contain actual text
    lValidSubs = [ s for s in oSubs if s.text.strip() ]
    iTotalValidSubs = len( lValidSubs )
    print(f"Starting translation: {iTotalValidSubs} lines in batches of {iBatchSize}.")

    # Start translation of input file
    for i in tqdm( range( 0, iTotalValidSubs, iBatchSize ), desc = "Batch Progress" ):
        lBatch = lValidSubs[ i : i + iBatchSize ]

        # Join lines with a unique separator
        sCombinedText = " |||| ".join( [s.text.replace("\n", " ") for s in lBatch] )

        try:
            # Translate text
            sTranslatedCombinedText = oTranslator.translate( sCombinedText )
            # Split translated string back into parts
            lTranslatedParts = sTranslatedCombinedText.split( "||||" )

            # Check if translation returned expected number of parts
            if len( lTranslatedParts ) == len( lBatch ):
                for j, sPart in enumerate( lTranslatedParts ):
                    lBatch[ j ].text = sPart.strip()
            else:
                # Fallback: if batching fails, translate lines one by one
                print(f"\nBatch {i//iBatchSize} misalignment. Falling back to individual translation for this group...")
                for s in lBatch:
                    s.text = oTranslator.translate( s.text )
                    time.sleep( 1 )

            # Small delay for the server
            time.sleep( 2 )

        except Exception as e:
            print(f"Error at line {i}: {e}. Waiting 10 seconds before retrying...")
            time.sleep(10)
        
    # Save result into new file
    oSubs.save( sOutputFile, encoding= sEncoding )
    print(f"✅ Translation complete: {sOutputFile}")


# Execute main logic
def main():
    sInputSrt, sOutputSrt, sTargetLanguage, sEncodingUsed = getArgumentsParsed()
    # print(f"input: {sInputSrt} | Output: {sOutputSrt} | Language: {sTargetLanguage} | Encoding used: {sEncodingUsed}")

    # Error handling 
    if not sInputSrt: 
        print( f"{ Colors.RED }[ERROR]{ Colors.ENDC } Input SRT file not specified." )
        return
    
    if not sOutputSrt:
        print( f"{ Colors.RED }[ERROR]{ Colors.ENDC } Output SRT file not specified." )
        return

    translateSrt( sInputSrt, sOutputSrt, sTargetLanguage, sEncodingUsed )


if __name__ == "__main__":
    main()
