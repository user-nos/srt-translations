import deepl
from tqdm import tqdm
import argparse
import pysubs2
import time

DEEPL_API_KEY = "your-free-api-key-here"

# Define color codes as constants for easier use
# Used for printing with colors in terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m' # Reset color

# Get arguments parsed from the terminal for the input srt file and the output srt file paths
# E.g. terminal >> python main.py -i abc.srt -o qwerty.srt -l(optional) "EN-US" -e(optional) "utf8"
def getArgumentsParsed():
    oParser = argparse.ArgumentParser(
        description="Get the arguments parsed from the terminal"
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
        default = "EN-US",
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
#                   E.g. path of input test srt file --> W:\Media\Movies\abc.srt
# sOutputFile   --> .srt file path and name where output file will written to
# sTargetLang   --> target language to translate to
# sEncoding     --> encoding used in the input srt for pysubs2 to load the file with (utf-8 or latin-1)
def translateSrt( sInputFile, sOutputFile, sTargetLang = "EN-US", sEncoding = "utf8" ):
    iBatchSize = 25
    # Initialize Translator object that was imported from the library "deepl"
    oTranslator = deepl.Translator( DEEPL_API_KEY )
    
    # Load input subs file
    oSubs = pysubs2.load( sInputFile, encoding = sEncoding )

    # Filter for lines that contain actual text
    lValidSubs = [ s for s in oSubs if s.text.strip() ]
    iTotalValidSubs = len( lValidSubs )
    print(f"Starting translation: {iTotalValidSubs} lines in batches of {iBatchSize}.")

    lBatchTexts = []

    # Start translation of input file
    for i in tqdm( range( 0, iTotalValidSubs, iBatchSize ), desc = "Batch Progress" ):
        lBatch = lValidSubs[ i : i + iBatchSize ]

        # Add lines to be translated into a batch
        for oSub in lBatch:
            sText = oSub.text.replace( "\n", " " )
            lBatchTexts.append( sText )

        try:
            # Translate text via DeepL API
            lTranslatedTexts = oTranslator.translate_text( lBatchTexts, target_lang = sTargetLang )

            # Assign translated texts back to the batch accordingly
            for j in range( len( lTranslatedTexts ) ):
                lBatch[ j ].text = lTranslatedTexts[ j ].text

        except Exception as e:
            print(f"Error at line {i}: {e}. Waiting 10 seconds before retrying...")
            time.sleep(10)

        lBatchTexts.clear()
        
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
