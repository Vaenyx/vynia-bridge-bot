use serde::Deserialize;

#[derive(Debug, Clone, Deserialize)]
pub struct Config {
    pub discord: DiscordConfig,
    pub urchin: UrchinConfig,
}

#[derive(Debug, Clone, Deserialize)]
pub struct DiscordConfig {
    pub token: String,
}

#[derive(Debug, Clone, Deserialize)]
pub struct UrchinConfig {
    pub api_key: String,
}

impl Config {
    pub fn from_env() -> Result<Self, envy::Error> {
        Ok(Self {
            discord: envy::prefixed("DISCORD_").from_env()?,
            urchin: envy::prefixed("URCHIN_").from_env()?,
        })
    }
}
