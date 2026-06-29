use serde::Deserialize;

#[derive(Debug, Clone, Deserialize)]
pub struct Config {
    pub discord: DiscordConfig,
    //pub minecraft: MinecraftConfig,
    //pub hypixel: HypixelConfig,
    //pub redis: RedisConfig,
    //pub commands: CommandConfig,
    pub urchin: UrchinConfig,
}

#[derive(Debug, Clone, Deserialize)]
pub struct DiscordConfig {
    pub token: String,
    pub guild_id: u64,
    pub bridge_channel_id: u64,
}

// #[derive(Debug, Clone, Deserialize)]
// pub struct MinecraftConfig {
//     pub email: String,
//     pub server: String,
// }
//
// #[derive(Debug, Clone, Deserialize)]
// pub struct HypixelConfig {
//     pub api_key: String,
// }
//
#[derive(Debug, Clone, Deserialize)]
pub struct UrchinConfig {
    pub api_key: String,
}
//
// #[derive(Debug, Clone, Deserialize)]
// pub struct RedisConfig {
//     pub url: String,
// }
//
// #[derive(Debug, Clone, Deserialize)]
// pub struct CommandConfig {
//     #[serde(default = "default_prefix")]
//     pub prefix: String,
// }
//
// fn default_prefix() -> String {
//     "!".to_string()
// }

impl Config {
    pub fn from_env() -> Result<Self, envy::Error> {
        dotenvy::dotenv().ok();

        Ok(Self {
            discord: envy::prefixed("DISCORD_").from_env()?,
            //minecraft: envy::prefixed("MINECRAFT_").from_env()?,
            //hypixel: envy::prefixed("HYPIXEL_").from_env()?,
            //redis: envy::prefixed("REDIS_").from_env()?,
            //commands: envy::prefixed("COMMAND_").from_env()?,
            urchin: envy::prefixed("URCHIN_").from_env()?,
        })
    }
}
