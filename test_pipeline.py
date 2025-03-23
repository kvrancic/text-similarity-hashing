import os
import subprocess
import sys
import difflib
import time

def run_tests(executable, test_dir):
    """
    Run tests for the specified executable using input files from test_dir.
    
    Args:
        executable (str): Path to the executable to test (Python script or compiled program)
        test_dir (str): Directory containing .in and .out files
    """
    # Get all .in files in the test directory
    in_files = [f for f in os.listdir(test_dir) if f.endswith('.in')]
    
    if not in_files:
        print(f"No input files found in {test_dir}")
        return
    
    print(f"Found {len(in_files)} test cases in {test_dir}")
    
    # Track results
    passed = 0
    failed = 0
    
    for in_file in sorted(in_files):
        base_name = in_file[:-3]  # Remove .in extension
        out_file = base_name + '.out'
        out_path = os.path.join(test_dir, out_file)
        
        if not os.path.exists(out_path):
            print(f"Warning: No output file found for {in_file}, skipping")
            continue
        
        in_path = os.path.join(test_dir, in_file)
        
        print(f"\nTesting {base_name}:")
        print("-" * 40)
        
        # Determine how to run the executable
        if executable.endswith('.py'):
            cmd = [sys.executable, executable]
        else:
            cmd = [executable]
        
        # Read expected output
        with open(out_path, 'r') as f:
            expected_output = f.read().strip()
        
        # Run the program with input file
        start_time = time.time()
        try:
            with open(in_path, 'r') as in_f:
                process = subprocess.run(
                    cmd,
                    stdin=in_f,
                    capture_output=True,
                    text=True,
                    timeout=300  # Timeout after 30 seconds
                )
            elapsed_time = time.time() - start_time
            
            actual_output = process.stdout.strip()
            error_output = process.stderr.strip()
            
            if error_output:
                print(f"Error output:\n{error_output}")
            
            # Compare outputs
            if actual_output == expected_output:
                print(f"✅ PASSED in {elapsed_time:.2f} seconds")
                passed += 1
            else:
                print(f"❌ FAILED in {elapsed_time:.2f} seconds")
                failed += 1
                
                # Show diff
                print("\nDifferences:")
                for line in difflib.unified_diff(
                    expected_output.splitlines(),
                    actual_output.splitlines(),
                    lineterm='',
                    fromfile='expected',
                    tofile='actual'
                ):
                    print(line)
                
                # Show outputs if not too long
                if len(expected_output) < 500 and len(actual_output) < 500:
                    print("\nExpected output:")
                    print(expected_output)
                    print("\nActual output:")
                    print(actual_output)
                
        except subprocess.TimeoutExpired:
            print(f"❌ TIMEOUT after 30 seconds")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            failed += 1
    
    # Print summary
    print("\n" + "=" * 40)
    print(f"Summary: {passed} passed, {failed} failed")
    print("=" * 40)
    
    return passed, len(in_files)

def main():
    if len(sys.argv) < 3:
        print("Usage: python test_pipeline.py <executable> <test_directory>")
        print("Example: python test_pipeline.py SimHash.py ./test_cases")
        sys.exit(1)
    
    executable = sys.argv[1]
    test_dir = sys.argv[2]
    
    if not os.path.exists(executable):
        print(f"Error: Executable '{executable}' not found")
        sys.exit(1)
    
    if not os.path.exists(test_dir) or not os.path.isdir(test_dir):
        print(f"Error: Test directory '{test_dir}' not found or is not a directory")
        sys.exit(1)
    
    run_tests(executable, test_dir)

if __name__ == "__main__":
    main()