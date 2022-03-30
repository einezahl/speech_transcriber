###
# The goal is to let one function create an infinite loop that is then 
# interrupted by a call from another function
# function 1: start loop
# function 2: stop loop
###
import asyncio

rec = True

async def start_loop():
	global rec
	while rec:
		await asyncio.sleep(1)
		print("Slept another second")
	print("Stopped loop")

def stop_loop():
	global rec
	rec = False
	print("Stopping loop")

async def main():
	loop = asyncio.get_event_loop()
	loop.create_task(start_loop())
	await asyncio.sleep(2)
	stop_loop()
	# loop.close()

asyncio.run(main())