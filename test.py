import concurrent.futures
import requests
import time
import json
from urllib.parse import urlencode

# Streamlit app URL
STREAMLIT_URL = "http://localhost:8501"

def test_streamlit_availability():
    """Test if Streamlit app is running and accessible"""
    try:
        response = requests.get(STREAMLIT_URL, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Streamlit app not accessible: {e}")
        return False

def simulate_research_request(session, idx, query="Test query"):
    """Simulate a research request by calling the agents module directly"""
    try:
        # Import and test the research function directly
        from agents import run_research
        start_time = time.time()
        
        # Run the research function
        result = run_research(query)
        
        elapsed = time.time() - start_time
        success = bool(result and len(str(result).strip()) > 0)
        
        return idx, success, elapsed, len(str(result))
    except Exception as e:
        return idx, False, 0, 0

def run_load_test(client_count=10, query="What is artificial intelligence?"):
    """Run load test on the research function"""
    print(f"Testing with {client_count} concurrent requests...")
    print(f"Query: {query}")
    print("-" * 50)
    
    # First check if Streamlit is running
    if not test_streamlit_availability():
        print("❌ Streamlit app is not running on localhost:8501")
        print("Please start it with: streamlit run app.py")
        return
    
    print("✅ Streamlit app is accessible")
    
    successes = 0
    total_time = 0
    total_chars = 0
    start = time.time()
    
    with requests.Session() as session:
        with concurrent.futures.ThreadPoolExecutor(max_workers=client_count) as executor:
            # Submit all tasks
            futures = [
                executor.submit(simulate_research_request, session, i, query) 
                for i in range(client_count)
            ]
            
            # Collect results
            for future in concurrent.futures.as_completed(futures):
                idx, success, elapsed, chars = future.result()
                if success:
                    successes += 1
                    total_time += elapsed
                    total_chars += chars
                    print(f"✅ Request {idx}: Success ({elapsed:.2f}s, {chars} chars)")
                else:
                    print(f"❌ Request {idx}: Failed")
    
    total_elapsed = time.time() - start
    
    print("-" * 50)
    print(f"📊 RESULTS:")
    print(f"Total requests: {client_count}")
    print(f"Successful: {successes}")
    print(f"Failed: {client_count - successes}")
    print(f"Success rate: {(successes/client_count)*100:.1f}%")
    print(f"Total time: {total_elapsed:.2f}s")
    print(f"Requests/sec: {client_count/total_elapsed:.2f}")
    
    if successes > 0:
        print(f"Average response time: {total_time/successes:.2f}s")
        print(f"Average response length: {total_chars/successes:.0f} characters")

def test_single_request():
    """Test a single request to verify everything works"""
    print(" Testing single request...")
    idx, success, elapsed, chars = simulate_research_request(None, 0, "What is machine learning?")
    
    if success:
        print(f"✅ Single request successful ({elapsed:.2f}s, {chars} chars)")
        return True
    else:
        print("❌ Single request failed")
        return False

if __name__ == "__main__":
    print(" Starting MCP Server Load Test")
    print("=" * 50)
    
    # Test single request first
    if test_single_request():
        print("\n" + "=" * 50)
        
        # Run load tests with different client counts
        test_cases = [5]
        
        for clients in test_cases:
            print(f"\n Testing with {clients} concurrent clients:")
            run_load_test(client_count=clients)
            print("\n" + "-" * 30)
            time.sleep(2)  # Brief pause between tests
    else:
        print("❌ Single request test failed. Please check your setup.")
