from fastmcp import FastMCP, Context
import json
import os

def register_resources(mcp: FastMCP):
    @mcp.resource(
        uri="data://users",
        name="UserData",
        description="Provides access to user data from local storage",
        mime_type="application/json"
    )
    async def user_data(ctx: Context) -> dict:
        """Retrieve all user records from the data storage system.
        
        This resource provides access to the complete user database in JSON format.
        Returns all stored users with their names and email addresses. The data
        is read directly from the storage file and formatted for easy consumption.
        
        Use this resource when you need to:
        - Display all users in an interface
        - Export user data for analysis
        - Verify user additions or modifications
        - Provide input data for other tools
        
        Returns:
            Dictionary containing:
            - users: Array of user objects, each with 'name' and 'email' fields
            
        Note: Returns empty array if no users exist or storage file is missing.
        """
        await ctx.debug("Accessing user data resource")
        
        users_file = "data/users.json"
        if os.path.exists(users_file):
            with open(users_file, 'r') as f:
                data = json.load(f)
            user_count = len(data.get("users", []))
            await ctx.info(f"Retrieved {user_count} users from storage")
            return {"users": data.get("users", [])}
        
        await ctx.warning("No users file found, returning empty list")
        return {"users": []}
    
    @mcp.resource(
        uri="data://users/{user_name}",
        name="SingleUser",
        description="Provides access to a specific user by name"
    )
    async def get_user_by_name(user_name: str, ctx: Context) -> dict:
        """Retrieve a specific user by their name from the data storage.
        
        This resource template allows you to fetch individual user records using
        their name as the identifier. The search is case-insensitive and looks
        for exact name matches in the user database.
        
        Access pattern: data://users/{user_name}
        Example: data://users/John%20Doe, data://users/Alice%20Johnson
        
        Args:
            user_name: The full name of the user to find (case-insensitive)
            
        Returns:
            Dictionary containing:
            - user: User object with 'name' and 'email' if found
            - error: Error message if user name not found
            
        Use this when you need to:
        - Fetch specific user details by their name
        - Look up user information for verification
        - Access individual users in a human-friendly way
        - Implement user search functionality
        
        Note: URL encode spaces and special characters in the name
        (e.g., "John Doe" becomes "John%20Doe" in the URL)
        """
        await ctx.debug(f"Searching for user with name: {user_name}")
        
        # URL decode the name in case it comes encoded
        import urllib.parse
        decoded_name = urllib.parse.unquote(user_name)
        
        users_file = "data/users.json"
        if os.path.exists(users_file):
            with open(users_file, 'r') as f:
                data = json.load(f)
                users = data.get("users", [])
                
                # Case-insensitive search for the user
                for user in users:
                    if user.get("name", "").lower() == decoded_name.lower():
                        await ctx.info(f"Found user: {user['name']}")
                        return {"user": user}
                        
                await ctx.warning(f"No user found with name: {decoded_name}")
        else:
            await ctx.warning("No users file found")
        
        await ctx.error(f"User not found with name: {decoded_name}")
        return {"user": None, "error": f"User '{decoded_name}' not found"}
    
    @mcp.resource(
        uri="data://users/stats",
        name="UserStats",
        description="Provides statistics about users in storage"
    )
    async def user_stats(ctx: Context) -> dict:
        """Generate comprehensive statistics about the user data storage.
        
        This resource provides detailed statistical analysis of all stored users,
        including domain distribution, name patterns, and data quality metrics.
        The analysis is performed with progress reporting for larger datasets.
        
        Useful for getting a quick overview of your user base demographics
        and identifying patterns in the data without running a full analysis.
        
        Returns:
            Dictionary containing:
            - stats: Object with statistical information including:
                - total: Total number of users
                - domains: Breakdown of email domains and their frequencies
                - most_common_domain: The most frequently used email domain
                - domain_count: Number of unique email domains
                - average_name_length: Average length of user names
        
        Use this resource when you need to:
        - Get quick demographic insights
        - Monitor user base diversity
        - Assess data quality at a glance
        - Generate summary reports
        - Track growth and patterns over time
        """
        await ctx.info("Generating user statistics")
        await ctx.report_progress(progress=0, total=100)
        
        users_file = "data/users.json"
        if not os.path.exists(users_file):
            await ctx.warning("No users file found for statistics")
            return {"stats": {"total": 0, "domains": {}}}
        
        # Stage 1: Load data (0-30%)
        await ctx.info("Loading user data...")
        with open(users_file, 'r') as f:
            data = json.load(f)
            users = data.get("users", [])
        
        await ctx.report_progress(progress=30, total=100)
        
        # Stage 2: Calculate basic stats (30-60%)
        await ctx.info("Calculating basic statistics...")
        total_users = len(users)
        domains = {}
        
        for i, user in enumerate(users):
            email = user.get("email", "")
            if "@" in email:
                domain = email.split("@")[1]
                domains[domain] = domains.get(domain, 0) + 1
            
            # Report progress for large datasets
            if total_users > 10:
                current_progress = 30 + (i * 30 // total_users)
                await ctx.report_progress(progress=current_progress, total=100)
        
        await ctx.report_progress(progress=60, total=100)
        
        # Stage 3: Calculate advanced stats (60-90%)
        await ctx.info("Calculating advanced statistics...")
        most_common_domain = max(domains, key=domains.get) if domains else None
        
        # Calculate name patterns
        name_lengths = [len(user.get("name", "")) for user in users]
        avg_name_length = sum(name_lengths) / len(name_lengths) if name_lengths else 0
        
        await ctx.report_progress(progress=90, total=100)
        
        # Stage 4: Finalize (90-100%)
        await ctx.info("Finalizing statistics...")
        await ctx.report_progress(progress=100, total=100)
        await ctx.info(f"Generated statistics for {total_users} users")
        
        return {
            "stats": {
                "total": total_users,
                "domains": domains,
                "most_common_domain": most_common_domain,
                "domain_count": len(domains),
                "average_name_length": round(avg_name_length, 2)
            }
        }
    
    @mcp.resource(
        uri="data://users/report",
        name="UserReport",
        description="Generates a comprehensive user report with progress tracking"
    )
    async def user_report(ctx: Context) -> dict:
        """Generate a comprehensive, detailed report about all user data.
        
        This resource performs an extensive analysis of the user database and
        generates a complete report including data validation, domain analysis,
        name patterns, and data quality assessment. The operation includes
        detailed progress tracking and is designed for thorough data auditing.
        
        This is the most comprehensive analysis available, going beyond basic
        statistics to provide actionable insights about data quality, user
        patterns, and potential issues that need attention.
        
        Returns:
            Dictionary containing:
            - report: Comprehensive report object with:
                - summary: Overview statistics (total, valid, invalid users)
                - domain_analysis: Detailed email domain breakdown
                - name_analysis: Name pattern statistics and insights
                - data_quality: Quality metrics and issue identification
        
        Use this resource when you need to:
        - Perform comprehensive data auditing
        - Generate detailed reports for stakeholders
        - Identify data quality issues for cleanup
        - Analyze user patterns for business intelligence
        - Prepare data for migration or integration
        - Conduct periodic data health assessments
        
        Note: This operation may take longer for large datasets due to
        comprehensive analysis with progress reporting.
        """
        await ctx.info("Starting comprehensive user report generation")
        await ctx.report_progress(progress=0, total=100)
        
        users_file = "data/users.json"
        if not os.path.exists(users_file):
            await ctx.warning("No users file found for report")
            return {"report": "No data available"}
        
        # Stage 1: Data loading and validation (0-20%)
        await ctx.info("Loading and validating user data...")
        with open(users_file, 'r') as f:
            data = json.load(f)
            users = data.get("users", [])
        
        valid_users = []
        invalid_users = []
        
        for user in users:
            if isinstance(user, dict) and "name" in user and "email" in user:
                valid_users.append(user)
            else:
                invalid_users.append(user)
        
        await ctx.report_progress(progress=20, total=100)
        
        # Stage 2: Domain analysis (20-50%)
        await ctx.info("Analyzing email domains...")
        domain_stats = {}
        for i, user in enumerate(valid_users):
            email = user.get("email", "")
            if "@" in email:
                domain = email.split("@")[1]
                domain_stats[domain] = domain_stats.get(domain, 0) + 1
            
            # Progress for large datasets
            if len(valid_users) > 5:
                current_progress = 20 + (i * 30 // len(valid_users))
                await ctx.report_progress(progress=current_progress, total=100)
        
        await ctx.report_progress(progress=50, total=100)
        
        # Stage 3: Name analysis (50-80%)
        await ctx.info("Analyzing user names...")
        name_stats = {
            "total_names": len(valid_users),
            "unique_names": len(set(user.get("name", "") for user in valid_users)),
            "avg_name_length": 0,
            "longest_name": "",
            "shortest_name": ""
        }
        
        if valid_users:
            names = [user.get("name", "") for user in valid_users]
            name_stats["avg_name_length"] = round(sum(len(name) for name in names) / len(names), 2)
            name_stats["longest_name"] = max(names, key=len)
            name_stats["shortest_name"] = min(names, key=len)
        
        await ctx.report_progress(progress=80, total=100)
        
        # Stage 4: Report compilation (80-100%)
        await ctx.info("Compiling final report...")
        report = {
            "summary": {
                "total_users": len(users),
                "valid_users": len(valid_users),
                "invalid_users": len(invalid_users)
            },
            "domain_analysis": domain_stats,
            "name_analysis": name_stats,
            "data_quality": {
                "validity_percentage": round((len(valid_users) / len(users)) * 100, 2) if users else 0,
                "issues_found": len(invalid_users)
            }
        }
        
        await ctx.report_progress(progress=100, total=100)
        await ctx.info("User report generation completed successfully")
        
        return {"report": report}