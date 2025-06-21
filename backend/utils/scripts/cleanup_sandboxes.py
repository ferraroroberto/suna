#!/usr/bin/env python
"""
Script to delete all STOPPED sandboxes to free up disk space.
"""

import asyncio
from sandbox.sandbox import daytona, SandboxState
from utils.logger import logger

async def delete_stopped_sandboxes():
    """
    List all sandboxes and delete those in STOPPED state.
    """
    try:
        # Get list of all sandboxes
        sandboxes = daytona.list()
        logger.info(f"Found {len(sandboxes)} sandboxes in total")
        
        # Filter for only stopped sandboxes
        stopped_sandboxes = [s for s in sandboxes if s.state == SandboxState.STOPPED]
        logger.info(f"Found {len(stopped_sandboxes)} stopped sandboxes that can be deleted")
        
        # Display sandboxes to be deleted
        for i, sandbox in enumerate(stopped_sandboxes):
            print(f"{i+1}. ID: {sandbox.id}")
            print(f"   Created: {sandbox.created_at}")
            print(f"   State: {sandbox.state}")
            print("-" * 40)
        
        # Confirm deletion
        if stopped_sandboxes:
            confirm = input(f"\nDelete all {len(stopped_sandboxes)} stopped sandboxes? (y/n): ")
            if confirm.lower() == 'y':
                # Delete each stopped sandbox
                deleted_count = 0                
                for sandbox in stopped_sandboxes:
                    try:
                        logger.info(f"Deleting sandbox {sandbox.id}...")
                        daytona.delete(sandbox)
                        print(f"✓ Successfully deleted sandbox {sandbox.id}")
                        deleted_count += 1
                    except Exception as e:
                        logger.error(f"Error deleting sandbox {sandbox.id}: {str(e)}")
                        print(f"✗ Failed to delete sandbox {sandbox.id}: {str(e)}")
                
                print(f"\nCleanup complete. Deleted {deleted_count} of {len(stopped_sandboxes)} sandboxes.")
            else:
                print("Deletion cancelled.")
        else:
            print("No stopped sandboxes to delete.")
            
    except Exception as e:
        logger.error(f"Error during sandbox cleanup: {str(e)}")
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # We don't actually need asyncio for this script since daytona calls are synchronous
    # But keeping the async pattern for consistency with other scripts
    asyncio.run(delete_stopped_sandboxes())
