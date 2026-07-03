use anyhow::Result;

mod apis;
mod commands;
mod config;
mod discord;
mod error;
mod minecraft;

#[tokio::main]
async fn main() -> Result<()> {
    dotenvy::dotenv().ok();

    let config = config::Config::from_env()?;

    let urchin_api = apis::urchin::UrchinApi::new(config.urchin.clone());

    let discord_task = discord::client::start_discord_bot(config.discord, urchin_api);

    //let minecraft_task = minecraft::client::start_minecraft_client(config.minecraft);

    tokio::select! {
        discord_result = discord_task => {
            discord_result?;
        }

        //minecraft_exit = minecraft_task => {
        //    println!("Minecraft client exited: {:?}", minecraft_exit);
        //}
    }

    Ok(())
}
