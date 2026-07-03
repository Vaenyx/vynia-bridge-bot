use azalea::prelude::*;

use crate::config::MinecraftConfig;

#[derive(Default, Clone, Component)]
pub struct State;

pub async fn start_minecraft_client(config: MinecraftConfig) -> AppExit {
    let account = Account::microsoft(&config.email)
        .await
        .expect("failed to login minecraft account");

    ClientBuilder::new()
        .set_handler(handle)
        .start(account, config.server)
        .await
}

async fn handle(bot: Client, event: Event, _state: State) -> eyre::Result<()> {
    match event {
        Event::Chat(message) => {
            println!("minecraft chat: {}", message.message().to_ansi());

            // later:
            // parse guild chat
            // forward to Discord
            // detect !commands
        }

        Event::Login => {
            println!("minecraft bot logged in");

            // later maybe:
            // bot.chat("/gc bot online");
        }

        _ => {}
    }

    return Ok(());
}
