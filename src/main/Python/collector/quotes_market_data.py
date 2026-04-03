"""
Quotes market data collector - fetches real-time quotes for all enabled symbols
and persists to JSON file. Runs continuously as a daemon.
"""
import sys
import os
import time
import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.api_client import initialize_fyers_client
from utils.json_handler import ensure_json_file, append_json_row
from utils.quotes_utils import parse_quotes_response
from config.collector_config import (
    QUOTES_DATA,
    POLLING_INTERVAL,
    QUOTES_MARKET_DATA_FILE,
)
def main():
    """Main function to collect and persist quotes data continuously."""
    try:
        # Initialize Fyers API client
        fyers, resources_pa"""
Quotes market data collector - fetches real-time quotes for all enabled symbols
and persists to JSON file. RunSOQufiand persists to JSON file. Runs continuously as a daemon.
"""
import sys
imporDA"""
import sys
import os
import time
import logging
      imloimport os(fimport tleimport loged# Configure la_logging.basicConfigg    level=logging.Iuo    format='%(asctime)on)
logger = logging.getLogger(__name__)
# Add parent directory toNG_I# Add parent directory to path for iosys.path.insert(0, os.path.dirname(os.pathifrom utils.api_client import initialize_fyers_client
from utif"from utils.json_handler import ensure_json_file, ap  from utils.quotes_utils import parse_quotes_response
from confi(dfrom config.collector_config import (
    QUOTES_DApo    QUOTES_DATA,
    POLLING_INTERVAPa    POLLING_INT d    QUOTES_MARKET_DAif)
def main():
    """Main fes_r    """Maisp    try:
        # Initialize Fyers API client
        fyers, resourcesrk       _p        fyers, resources_pa"""
QuotedaQuotes market data collector   and persists to JSON file. RunSOQufiand persists to JSON file. Runs continuous_r"""
import sys
imporDA"""
import sys
import os
import time
import logging
      imloimport o  im  imporDA"":
import sy  import osloimport tniimport log t      imloimps logger = logging.getLogger(__name__)
# Add parent directory toNG_I# Add parent directory to path for iosys.path.insert(0, o  # Add parent directory toNG_I# Add   from utif"from utils.json_handler import ensure_json_file, ap  from utils.quotes_utils import parse_quotes_response
from confi(dfrom config.collector_config imp  from confi(dfrom config.collector_config import (
    QUOTES_DApo    QUOTES_DATA,
    POLLING_INTERVAPa    POLLINGf"    QUOTES_DApo    QUOTES_DATA,
    POLLING_INTE      POLLING_INTERVAPa    POLLI{mdef main():
    """Main fes_r    """Maisp    try:
        # .c    """MaiCr        # Initialize Fyers API clienr:        fyers, resourcesrk       _p ifQuotedaQuotes market data collector   anpython -m py_compile /Users/lalitpatil/IdeaProjects/MarketDataEngineering/src/main/Python/collector/quotes_market_data.py /Users/lalitpatil/IdeaProjects/MarketDataEngineering/src/main/Python/collector/history_market_data.py
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python -m py_compile src/main/Python/collector/quotes_market_data.py src/main/Python/collector/history_market_data.py
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python -m py_compile src/main/Python/utils/logger.py src/main/Python/collector/quotes_market_data.py src/main/Python/collector/history_market_data.py
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python -m pytest src/test/test_auth.py -v
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python -m unittest src.test.test_auth -v
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python -m py_compile src/test/test_auth.py && python -c "import sys; sys.path.insert(0, 'src/main/Python'); import unittest; loader = unittest.TestLoader(); suite = loader.discover('src/test', pattern='test_auth.py'); runner = unittest.TextTestRunner(verbosity=2); runner.run(suite)"
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python -m py_compile src/test/test_auth.py && echo "✓ Syntax valid"
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python3 -m py_compile src/test/test_auth.py && echo "Test syntax is valid"
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python -m py_compile src/test/test_history_market_data.py && echo "✓ Test file syntax is valid"
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python3 -m py_compile src/test/test_history_market_data.py && echo "✓ Syntax valid"
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python -m py_compile src/test/test_history_market_data.py && echo "✓ Syntax valid"
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python3 -m py_compile src/test/test_history_market_data.py && python3 -m unittest src.test.test_history_market_data.TestParseCandles -v 2>&1 | head -50
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python -m unittest src.test.test_history_market_data.TestParseCandles.test_parse_candles_with_valid_response -v
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python -m unittest src.test.test_history_market_data -v 2>&1 | tail -100
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python -m unittest src.test.test_history_market_data 2>&1
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python src/test/test_history_market_data.py 2>&1 | head -200
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python -m py_compile src/test/test_history_market_data.py && echo "✓ Syntax valid"
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python -m unittest discover -s src/test -p 'test_history_market_data.py' -v 2>&1 | grep -E "(test_|OK|FAILED|ERROR)" | head -50
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python -m pytest src/test/test_history_market_data.py -v --tb=short 2>&1 | head -100
cd /Users/lalitpatil/IdeaProjects/MarketDataEngineering && python3 << 'EOF'
import sys
sys.path.insert(0, 'src/main/Python')
import unittest
from src.test.test_history_market_data import TestParseCandles, TestHistoryMarketDataMain, TestHistoryDataIntegration
loader = unittest.TestLoader()
suite = unittest.TestSuite()
suite.addTests(loader.loadTestsFromTestCase(TestParseCandles))
suite.addTests(loader.loadTestsFromTestCase(TestHistoryMarketDataMain))
suite.addTests(loader.loadTestsFromTestCase(TestHistoryDataIntegration))
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
print(f"\n\nTests run: {result.testsRun}")
print(f"Failures: {len(result.failures)}")
print(f"Errors: {len(result.errors)}")
if result.failures:
    print("\nFailures:")
    for test, traceback in result.failures:
        print(f"\n{test}:\n{traceback}")
if result.errors:
    print("\nErrors:")
    for test, traceback in result.errors:
        print(f"\n{test}:\n{traceback}")
