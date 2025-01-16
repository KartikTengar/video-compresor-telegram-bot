import asyncio
import imageio_ffmpeg as ffmpeg
import os
import time

async def compress_video(input_file, output_file, crf_value, thread_count):
    if os.path.exists(output_file):
        os.remove(output_file)

    ffmpeg_path = ffmpeg.get_ffmpeg_exe()
    
    start_time = time.time()
    
    process = await asyncio.create_subprocess_exec(
        ffmpeg_path, "-i", input_file,
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", str(crf_value),
        "-tune", "film",
        "-profile:v", "high",
        "-level", "4.1",
        "-threads", str(thread_count),
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_file,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    try:
        stdout, stderr = await process.communicate()
        end_time = time.time()
        duration = end_time - start_time
        
        if process.returncode == 0:
            input_size = os.path.getsize(input_file) / (1024 * 1024)
            output_size = os.path.getsize(output_file) / (1024 * 1024)
            
            return {
                'success': True,
                'duration': duration,
                'input_size': input_size,
                'output_size': output_size,
                'threads': thread_count
            }
        else:
            return {
                'success': False,
                'error': stderr.decode(),
                'threads': thread_count
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'threads': thread_count
        }

async def test_different_threads(input_file, thread_counts):
    results = []
    for threads in thread_counts:
        output_file = f"output_{threads}threads.mp4"
        print(f"\nTesting with {threads} threads...")
        
        result = await compress_video(input_file, output_file, 23, threads)
        
        if result['success']:
            print(f"Threads: {threads}")
            print(f"Duration: {result['duration']:.2f} seconds")
            print(f"Input size: {result['input_size']:.2f} MB")
            print(f"Output size: {result['output_size']:.2f} MB")
            print(f"Compression ratio: {(1 - result['output_size']/result['input_size']) * 100:.2f}%")
            results.append(result)
        else:
            print(f"Failed with {threads} threads:")
            print(result['error'])
        
        if os.path.exists(output_file):
            os.remove(output_file)
            
    return results

thread_counts = [1, 2, 4, 6, 8]
input_file = "downloads/Downloaded.mp4"

try:
    results = asyncio.run(test_different_threads(input_file, thread_counts))
    
    if results:
        print("\nFinal Results:")
        print("Threads | Duration (s) | Compression Ratio")
        print("-" * 45)
        for r in results:
            ratio = (1 - r['output_size']/r['input_size']) * 100
            print(f"{r['threads']:7d} | {r['duration']:11.2f} | {ratio:16.2f}%")
            
        best_result = min(results, key=lambda x: x['duration'])
        print(f"\nBest performance with {best_result['threads']} threads: {best_result['duration']:.2f} seconds")
        
except KeyboardInterrupt:
    print("\nTesting cancelled by user")
except Exception as e:
    print(f"Error: {str(e)}")