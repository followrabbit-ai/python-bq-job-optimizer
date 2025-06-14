from rabbit_bq_job_optimizer import RabbitBQOptimizer, OptimizationConfig

def main():
    # Initialize the client
    client = RabbitBQOptimizer(
        api_key="...", # Your Rabbit API key
        base_url="..."  # Your Rabbit API base URL
    )

    query = "SELECT * FROM `region-EU.INFORMATION_SCHEMA.JOBS`"

    # Example BigQuery job configuration
    jobConfig = {
        "configuration": {
            "query": {
                "query": query,
                "useLegacySql": False,
                "priority": "INTERACTIVE"
            }
        }
    }

    # Example optimization configuration
    optimizationConfig = OptimizationConfig(
        type="reservation_assignment",
        config={
            "defaultPricingMode": "on_demand",
            "reservationIds": [ # Your reservation IDs in the format "project:region.reservation-name". 
                "...",          # One for each region you want to optimize for.
                "..." 
            ]
        }
    )

    try:
        # Optimize the job
        result = client.optimize_job(
            configuration=jobConfig,
            enabledOptimizations=[optimizationConfig]
        )

        # Print results
        print("Optimization Results:")
        print(f"Optimization Performed: {result.optimizationPerformed}")
        print(f"Estimated Savings: ${result.estimatedSavings:.2f}")

        for optimization in result.optimizationResults:
            print(f"\nOptimization Type: {optimization.type}")
            print(f"Performed: {optimization.performed}")
            print(f"Estimated Savings: ${optimization.estimatedSavings:.2f}")
            print("Context:")
            for key, value in optimization.context.items():
                print(f"  {key}: {value}")

        print("\nOptimized Configuration:")
        print(result.optimizedJob)

        # Send optimized configuration to BigQuery
        from google.cloud import bigquery
        
        # Initialize BigQuery client
        bq_client = bigquery.Client()
        
        # Create job from optimized configuration
        job = bq_client.create_job(result.optimizedJob['configuration'])
        
        # Execute the job
        job_result = job.result()  # Waits for job to complete
        
        print("\nBigQuery Job Results:")
        print(f"Job ID: {job.job_id}")
        print(f"State: {job.state}")
        print(f"Result: {job_result}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 