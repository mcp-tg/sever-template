from fastmcp import FastMCP, Context

def register_prompts(mcp: FastMCP):
    @mcp.prompt(
        name="user_management_assistant",
        description="Template for user data management assistant"
    )
    async def user_data_template(ctx: Context) -> str:
        """Generate a comprehensive assistant prompt for user data management.
        
        This prompt template creates a detailed instruction set for AI assistants
        to effectively help users manage their data using this MCP server. The
        prompt includes current system status, available tools and resources,
        and guidance for common workflows.
        
        The prompt dynamically includes the current user count to provide
        real-time context about the system state, making assistant responses
        more relevant and informed.
        
        Returns:
            String containing a complete prompt template that:
            - Explains the assistant's role and capabilities
            - Lists all available tools with descriptions
            - Describes accessible resources and their purposes  
            - Provides current system status information
            - Suggests efficient workflows and best practices
        
        Use this prompt when:
        - Setting up AI assistants for user data management
        - Providing context for automated data operations
        - Training assistants on available server capabilities
        - Establishing consistent assistant behavior patterns
        """
        await ctx.info("Generating user management assistant prompt")
        
        # Get current user count for context
        try:
            user_data = await ctx.read_resource("data://users")
            current_count = len(user_data.get("users", []))
            await ctx.debug(f"Current user count: {current_count}")
        except:
            current_count = 0
            await ctx.warning("Could not retrieve current user count")
        
        return f"""
        You are an assistant that helps manage user data stored in local files.
        
        Current system status: {current_count} users in storage
        
        Available tools:
        - write_user: Adds a new user to the data storage (requires name and email)
        - get_user_count: Returns the total number of users in storage
        - analyze_users: Analyze user data and provide insights
        
        Available resources:
        - data://users: Returns all users from the data storage
        - data://users/{{user_id}}: Returns a specific user by ID
        - data://users/stats: Returns statistics about users
        
        Please help the user manage their data efficiently using the file-based storage system.
        """
    
    @mcp.prompt(
        name="data_analysis_prompt",
        description="Template for analyzing user data"
    )
    async def analyze_user_data(analysis_type: str = "summary", ctx: Context = None) -> str:
        """Generate a tailored prompt for user data analysis with contextual information.
        
        This prompt template creates analysis-specific instructions that incorporate
        current system statistics and data context. The prompt adapts based on the
        requested analysis type and includes relevant data overview information
        to guide more effective analysis.
        
        Args:
            analysis_type: Type of analysis to perform (default: "summary")
                - "summary": General overview and key insights
                - "detailed": Comprehensive analysis with deep insights  
                - "quality": Focus on data quality and validation
                - "demographic": Focus on user patterns and demographics
                
        Returns:
            String containing a customized analysis prompt that:
            - Specifies the requested analysis type and approach
            - Includes current data context and statistics
            - Provides guidance on what insights to focus on
            - Suggests specific areas to examine based on data state
        
        Use this prompt for:
        - Guiding AI assistants in data analysis tasks
        - Ensuring consistent analysis approaches
        - Providing context-aware analysis instructions
        - Standardizing analysis reporting formats
        """
        if ctx:
            await ctx.info(f"Generating {analysis_type} analysis prompt")
            
            # Get current stats for context
            try:
                stats_data = await ctx.read_resource("data://users/stats")
                stats = stats_data.get("stats", {})
                await ctx.debug(f"Current stats: {stats}")
            except:
                stats = {}
                await ctx.warning("Could not retrieve current stats")
        else:
            stats = {}
        
        stats_context = ""
        if stats:
            total = stats.get("total", 0)
            domains = stats.get("domains", {})
            stats_context = f"\n\nCurrent data overview: {total} users with domains: {list(domains.keys())}"
        
        return f"""
        Please perform a {analysis_type} analysis of the user data.
        
        Use the data://users resource to access all user information.
        Focus on providing insights about user patterns, email domains, and data quality.
        {stats_context}
        """
    
    @mcp.prompt(
        name="interactive_user_prompt",
        description="Interactive prompt that can elicit user information"
    )
    async def interactive_user_setup(ctx: Context) -> str:
        """Create a personalized, interactive prompt for user onboarding and setup.
        
        This prompt template uses client elicitation to gather user preferences
        and create a customized assistant experience. It interactively asks users
        about their needs and preferences, then generates a tailored prompt that
        addresses their specific use case.
        
        The prompt uses MCP's elicitation capabilities to engage users in a
        conversation about their requirements, then creates a personalized
        assistant configuration based on their responses.
        
        Returns:
            String containing a personalized prompt that:
            - Addresses the user by name (gathered via elicitation)
            - Reflects their stated preferences and needs
            - Provides relevant guidance based on their requirements
            - Suggests appropriate workflows for their use case
            - Offers next steps tailored to their situation
        
        Use this prompt for:
        - Onboarding new users to the system
        - Creating personalized assistant experiences
        - Gathering user requirements and preferences
        - Demonstrating interactive MCP capabilities
        - Setting up context-aware assistant sessions
        
        Note: This prompt requires an interactive client that supports
        elicitation (ctx.elicit). It may not work in all environments.
        """
        await ctx.info("Creating interactive user setup prompt")
        
        # Elicit user preferences
        user_name = await ctx.elicit("What is your name?", response_type=str)
        analysis_level = await ctx.elicit("What level of analysis do you want? (basic/detailed)", response_type=str)
        
        await ctx.info(f"Interactive setup completed for {user_name}")
        
        return f"""
        Hello {user_name}! I'm here to help you manage your user data.
        
        Based on your preference for {analysis_level} analysis, I'll adjust my responses accordingly.
        
        You can ask me to:
        - Add new users to the system
        - Analyze existing user data
        - Get statistics about your users
        - Retrieve specific user information
        
        What would you like to do first?
        """