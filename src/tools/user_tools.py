from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
import json
import os

def register_tools(mcp: FastMCP):
    @mcp.tool(
        name="write_user",
        description="Add a new user to the data storage",
        tags={"user", "storage"}
    )
    async def write_user(name: str, email: str, ctx: Context) -> dict:
        """Add a new user to the data storage system.
        
        This tool creates a new user record with the provided name and email address.
        The user data is stored in a JSON file (data/users.json) and can be retrieved
        using the data://users resource or analyzed using the analyze_users tool.
        
        Args:
            name: Full name of the user (required, should be 2+ characters)
            email: Valid email address (required, must contain @ and .)
            
        Returns:
            Dictionary with status "success" and confirmation message, or error details
            
        Example usage:
            - Add individual users one at a time
            - For multiple users, consider using bulk_add_users instead
            - Follow up with get_user_count to verify the addition
        """
        await ctx.info(f"Adding new user: {name} with email: {email}")
        
        try:
            users_file = "data/users.json"
            users = []
            
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    data = json.load(f)
                    users = data.get("users", [])
            
            await ctx.debug(f"Current user count: {len(users)}")
            
            users.append({"name": name, "email": email})
            
            with open(users_file, 'w') as f:
                json.dump({"users": users}, f, indent=2)
            
            await ctx.info(f"User {name} successfully added. Total users: {len(users)}")
            return {"status": "success", "message": f"User {name} added"}
        except (json.JSONDecodeError, IOError) as e:
            await ctx.error(f"Failed to add user {name}: {str(e)}")
            raise ToolError(f"File error: {str(e)}")
    
    @mcp.tool(
        name="get_user_count",
        description="Get the total number of users in storage"
    )
    async def get_user_count(ctx: Context) -> int:
        """Get the total number of users currently stored in the system.
        
        This tool provides a quick count of all users in the data storage without
        returning the actual user data. Useful for monitoring growth, checking
        if users exist before analysis, or verifying bulk operations.
        
        Args:
            None required
            
        Returns:
            Integer count of total users (0 if no users or file doesn't exist)
            
        Example usage:
            - Check if any users exist before running analysis
            - Monitor user growth over time
            - Verify bulk_add_users operation results
            - Quick status check without loading full user data
        """
        await ctx.debug("Retrieving user count from storage")
        
        users_file = "data/users.json"
        if os.path.exists(users_file):
            with open(users_file, 'r') as f:
                data = json.load(f)
                count = len(data.get("users", []))
                await ctx.info(f"User count retrieved: {count}")
                return count
        
        await ctx.info("No users file found, returning 0")
        return 0
    
    @mcp.tool(
        name="analyze_users",
        description="Analyze user data and provide insights",
        tags={"user", "analysis"}
    )
    async def analyze_users(ctx: Context) -> dict:
        """Perform comprehensive analysis of all user data and generate insights.
        
        This tool examines all stored users and generates detailed insights through
        a combination of statistical analysis and AI-powered strategic insights:
        - Email domain distribution and diversity analysis
        - Name length statistics and patterns  
        - Data quality assessment and recommendations
        - AI-generated strategic insights for business intelligence
        
        The analysis includes both local statistical computations and optional
        AI-powered insights via LLM sampling when available. Includes detailed
        progress reporting for longer operations.
        
        Args:
            None required
            
        Returns:
            Dictionary containing:
            - total_users: Count of users analyzed
            - email_domains: Breakdown of domains and their frequency
            - insights: Array combining statistical findings and AI insights
            
        Example usage:
            - Run after adding users to understand demographics
            - Generate strategic insights for business planning
            - Data quality assessment before important operations
            - AI-powered market analysis and growth recommendations
            
        Note: AI insights require an LLM-capable client. Falls back to
        statistical analysis only if AI sampling is unavailable.
        """
        await ctx.info("Starting user data analysis")
        
        try:
            # Stage 1: Data loading (0-20%)
            await ctx.report_progress(progress=0, total=100)
            await ctx.info("Loading user data...")
            
            # Read user data directly from file
            users_file = "data/users.json"
            users = []
            
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    data = json.load(f)
                    users = data.get("users", [])
                await ctx.info(f"Loaded {len(users)} users from file")
            else:
                await ctx.warning("No users file found")
            
            if not users:
                await ctx.warning("No users found for analysis")
                return {"analysis": "No users to analyze"}
            
            await ctx.report_progress(progress=20, total=100)
            
            # Stage 2: Domain analysis (20-60%)
            await ctx.info("Analyzing email domains...")
            domains = {}
            for i, user in enumerate(users):
                email = user.get("email", "")
                if "@" in email:
                    domain = email.split("@")[1]
                    domains[domain] = domains.get(domain, 0) + 1
                
                # Report progress for each user processed
                current_progress = 20 + (i * 40 // len(users))
                await ctx.report_progress(progress=current_progress, total=100)
            
            await ctx.report_progress(progress=60, total=100)
            
            # Stage 3: Generate insights (60-90%)
            await ctx.info("Generating insights...")
            
            # First generate basic insights
            basic_insights = []
            
            if domains:
                most_common_domain = max(domains, key=domains.get)
                domain_count = len(domains)
                basic_insights.append(f"Found {domain_count} unique email domains")
                basic_insights.append(f"Most common domain: {most_common_domain} ({domains[most_common_domain]} users)")
                
                if domain_count > 3:
                    basic_insights.append("Good diversity in email domains")
                elif domain_count == 1:
                    basic_insights.append("All users from single domain - consider expanding reach")
            
            # Name analysis
            names = [user.get("name", "") for user in users if user.get("name")]
            if names:
                avg_name_length = sum(len(name) for name in names) / len(names)
                basic_insights.append(f"Average name length: {avg_name_length:.1f} characters")
                
                if avg_name_length > 15:
                    basic_insights.append("Users tend to have longer names")
                elif avg_name_length < 8:
                    basic_insights.append("Users tend to have shorter names")
            
            # Data quality insights
            valid_emails = sum(1 for user in users if "@" in user.get("email", ""))
            if valid_emails < len(users):
                basic_insights.append(f"Data quality issue: {len(users) - valid_emails} users with invalid emails")
            else:
                basic_insights.append("All users have valid email format")
            
            await ctx.report_progress(progress=75, total=100)
            
            # Stage 4: AI-powered insights (75-90%)
            await ctx.info("Generating AI-powered insights...")
            ai_insights = []
            
            try:
                # Use LLM sampling for deeper insights
                analysis_prompt = f"""Analyze this user data and provide strategic insights:

                Data Summary:
                - Total users: {len(users)}
                - Email domains: {domains}
                - Basic insights: {basic_insights}

                Please provide 3-5 strategic insights about:
                1. User acquisition patterns
                2. Market reach and diversity
                3. Potential growth opportunities
                4. Data quality recommendations

                Keep insights concise and actionable.
            """
                
                ai_response = await ctx.sample(analysis_prompt, temperature=0.3)
                ai_insights.append("AI-Powered Strategic Insights:")
                ai_insights.append(ai_response)
                
            except Exception as e:
                await ctx.warning(f"AI insights unavailable: {str(e)}")
                ai_insights.append("AI insights not available in this environment")
            
            # Combine all insights
            insights = basic_insights + ai_insights
            
            await ctx.report_progress(progress=90, total=100)
            
            # Stage 4: Finalization (90-100%)
            await ctx.info("Finalizing analysis...")
            await ctx.report_progress(progress=100, total=100)
            await ctx.info("User analysis completed successfully")
            
            return {
                "total_users": len(users),
                "email_domains": domains,
                "insights": insights
            }
            
        except Exception as e:
            await ctx.error(f"Analysis failed: {str(e)}")
            raise ToolError(f"Analysis error: {str(e)}")
    
    @mcp.tool(
        name="bulk_add_users",
        description="Add multiple users to storage with progress tracking",
        tags={"user", "bulk", "storage"}
    )
    async def bulk_add_users(users_data: list[dict], ctx: Context) -> dict:
        """Add multiple users efficiently with detailed progress tracking.
        
        This tool processes an array of user objects and adds them to storage
        with comprehensive progress reporting and error handling. Each user
        is validated individually, and the operation continues even if some
        users fail validation.
        
        Designed for scenarios where you need to import or migrate user data
        from external sources, with detailed reporting of successes and failures.
        
        Args:
            users_data: Array of user objects, each containing:
                - name: User's full name (string, required)
                - email: User's email address (string, required)
                
        Returns:
            Dictionary containing:
            - status: "completed" when finished
            - total_processed: Number of users attempted
            - successful: Count of successfully added users
            - failed: Count of failed user additions
            - errors: Array of error messages for failed users
            
        Example usage:
            - Import users from CSV/external systems
            - Migrate user data between systems
            - Batch user creation for testing/demos
            - Any scenario requiring multiple user additions
        """
        await ctx.info(f"Starting bulk addition of {len(users_data)} users")
        
        if not users_data:
            return {"status": "success", "message": "No users to add"}
        
        # Initialize progress
        total_users = len(users_data)
        successful_adds = 0
        failed_adds = 0
        errors = []
        
        await ctx.report_progress(progress=0, total=total_users)
        
        # Load existing users
        users_file = "data/users.json"
        existing_users = []
        
        if os.path.exists(users_file):
            with open(users_file, 'r') as f:
                data = json.load(f)
                existing_users = data.get("users", [])
        
        # Process each user
        for i, user_data in enumerate(users_data):
            try:
                # Validate user data
                if not isinstance(user_data, dict) or "name" not in user_data or "email" not in user_data:
                    raise ValueError("Invalid user data format")
                
                # Add user
                existing_users.append({
                    "name": user_data["name"],
                    "email": user_data["email"]
                })
                
                successful_adds += 1
                await ctx.info(f"Added user: {user_data['name']}")
                
            except Exception as e:
                failed_adds += 1
                error_msg = f"Failed to add user {user_data.get('name', 'Unknown')}: {str(e)}"
                errors.append(error_msg)
                await ctx.warning(error_msg)
            
            # Report progress after each user
            await ctx.report_progress(progress=i + 1, total=total_users)
        
        # Save all users
        try:
            with open(users_file, 'w') as f:
                json.dump({"users": existing_users}, f, indent=2)
            await ctx.info("All users saved to storage")
        except Exception as e:
            await ctx.error(f"Failed to save users: {str(e)}")
            raise ToolError(f"Storage error: {str(e)}")
        
        return {
            "status": "completed",
            "total_processed": total_users,
            "successful": successful_adds,
            "failed": failed_adds,
            "errors": errors
        }
    
    @mcp.tool(
        name="process_users_simulation",
        description="Simulate a long-running user processing task",
        tags={"user", "simulation", "demo"}
    )
    async def process_users_simulation(duration_seconds: int, ctx: Context) -> dict:
        """Simulate a long-running task with indeterminate progress."""
        import asyncio
        
        await ctx.info(f"Starting {duration_seconds}-second simulation")
        
        # Simulate work in small chunks
        chunks = max(1, duration_seconds * 10)  # 10 updates per second
        chunk_duration = duration_seconds / chunks
        
        for i in range(chunks):
            # Simulate work
            await asyncio.sleep(chunk_duration)
            
            # Report progress
            await ctx.report_progress(progress=i + 1, total=chunks)
            
            # Occasional status updates
            if (i + 1) % 10 == 0:
                percentage = ((i + 1) / chunks) * 100
                await ctx.info(f"Processing... {percentage:.1f}% complete")
        
        await ctx.info("Simulation completed successfully")
        return {
            "status": "completed",
            "duration": duration_seconds,
            "chunks_processed": chunks
        }