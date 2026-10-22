from sustaingym.envs.battery_storage import ElectricityMarketEnv

# Crear la instancia del entorno
env = ElectricityMarketEnv(month='2021-05', use_intermediate_rewards=False)
obs, info = env.reset(seed=123)

print("✅ ¡Entorno cargado exitosamente desde battery_storage!")