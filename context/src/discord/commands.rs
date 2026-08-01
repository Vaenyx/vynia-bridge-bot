use crate::apis::urchin::{CustomSession, Period};
use crate::commands::bedwars::get_bw_custom_stats;
use crate::discord::formatting::{bedwars_period_embed, bedwars_session_embed};
use crate::discord::{Context, Error};

#[poise::command(slash_command)]
pub async fn ping(ctx: Context<'_>) -> Result<(), Error> {
    ctx.say("pong").await?;
    return Ok(());
}

#[poise::command(slash_command)]
pub async fn bwsession(
    ctx: Context<'_>,
    username: String,

    #[description = "Example: 24h, 7d, 2w, 200000h"] duration: Option<String>,

    #[description = "Unix timestamp in milliseconds, example: 1719878400000"] from_ms: Option<i64>,
) -> Result<(), Error> {
    ctx.defer().await?;

    let session = match (duration, from_ms) {
        (Some(_), Some(_)) => {
            ctx.say("Use either `duration` or `from_ms`, not both.")
                .await?;
            return Ok(());
        }

        (Some(duration), None) => CustomSession::Duration(duration),

        (None, Some(from_ms)) => CustomSession::FromMs(from_ms),

        (None, None) => {
            ctx.say("Use either `duration` or `from_ms`.").await?;
            return Ok(());
        }
    };

    let stats = get_bw_custom_stats(&ctx.data().urchin, &username, session).await?;
    let embed = bedwars_session_embed(&stats, "Custom Session");

    ctx.send(poise::CreateReply::default().embed(embed)).await?;

    return Ok(());
}

#[poise::command(slash_command)]
pub async fn daily(ctx: Context<'_>, username: String) -> Result<(), Error> {
    send_bedwars_period(ctx, username, Period::Daily).await
}

#[poise::command(slash_command)]
pub async fn weekly(ctx: Context<'_>, username: String) -> Result<(), Error> {
    send_bedwars_period(ctx, username, Period::Weekly).await
}

#[poise::command(slash_command)]
pub async fn monthly(ctx: Context<'_>, username: String) -> Result<(), Error> {
    send_bedwars_period(ctx, username, Period::Monthly).await
}

#[poise::command(slash_command)]
pub async fn yearly(ctx: Context<'_>, username: String) -> Result<(), Error> {
    send_bedwars_period(ctx, username, Period::Yearly).await
}

async fn send_bedwars_period(
    ctx: Context<'_>,
    username: String,
    period: Period,
) -> Result<(), Error> {
    ctx.defer().await?;

    let duration = format!("{}h", period.as_hours());

    let stats = get_bw_custom_stats(
        &ctx.data().urchin,
        &username,
        CustomSession::Duration(duration),
    )
    .await?;

    let embed = bedwars_period_embed(&stats, period);

    ctx.send(poise::CreateReply::default().embed(embed)).await?;

    return Ok(());
}
