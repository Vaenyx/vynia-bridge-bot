use poise::serenity_prelude::{CreateEmbed, CreateEmbedFooter};

use crate::apis::urchin::{Period, SessionResponse};

pub fn bedwars_period_embed(session: &SessionResponse, period: Period) -> CreateEmbed {
    return bedwars_session_embed(session, period.label());
}

pub fn bedwars_session_embed(session: &SessionResponse, label: impl AsRef<str>) -> CreateEmbed {
    let bw = &session.delta.stats.bedwars;
    let label = label.as_ref();

    let name = clean_minecraft_name(&session.displayname);

    let wlr = ratio(bw.wins_bedwars, bw.losses_bedwars);
    let fkdr = ratio(bw.final_kills_bedwars, bw.final_deaths_bedwars);
    let kdr = ratio(bw.kills_bedwars, bw.deaths_bedwars);
    let bblr = ratio(bw.beds_broken_bedwars, bw.beds_lost_bedwars);

    let games = bw.games_played_bedwars;

    let stars_gained = bw.experience as f64 / 5000.0;

    let skin_url = format!("https://mc-heads.net/avatar/{}/128.png", session.uuid);

    return CreateEmbed::new()
        .title(format!("{name} — {label} Bedwars Stats"))
        .thumbnail(skin_url)
        .field(
            "Ratios",
            format!(
                "**WLR:** `{wlr:.2}`\n\
                 **FKDR:** `{fkdr:.2}`\n\
                 **KDR:** `{kdr:.2}`\n\
                 **BBLR:** `{bblr:.2}`"
            ),
            true,
        )
        .field(
            "Combat",
            format!(
                "**Kills:** `+{}`\n\
                 **Deaths:** `+{}`\n\
                 **Finals:** `+{}`\n\
                 **FDeaths:** `+{}`",
                bw.kills_bedwars,
                bw.deaths_bedwars,
                bw.final_kills_bedwars,
                bw.final_deaths_bedwars,
            ),
            true,
        )
        .field(
            "Games",
            format!(
                "**Wins:** `+{}`\n\
                 **Losses:** `+{}`\n\
                 **Games:** `+{}`\n\
                 **Stars:** `+{:.2}★`",
                bw.wins_bedwars, bw.losses_bedwars, games, stars_gained,
            ),
            true,
        )
        .field(
            "Beds",
            format!(
                "**Beds Broken:** `+{}`\n\
                 **Beds Lost:** `+{}`",
                bw.beds_broken_bedwars, bw.beds_lost_bedwars,
            ),
            true,
        )
        .footer(CreateEmbedFooter::new(format!(
            "Since {}",
            session.from_readable
        )));
}

fn ratio(good: u32, bad: u32) -> f64 {
    match (good, bad) {
        (0, 0) => 0.0,
        (_, 0) => good as f64,
        _ => good as f64 / bad as f64,
    }
}

fn clean_minecraft_name(input: &str) -> String {
    let mut out = String::new();
    let mut skip_next = false;

    for ch in input.chars() {
        if skip_next {
            skip_next = false;
            continue;
        }

        if ch == '§' || ch == '&' || ch == '$' {
            skip_next = true;
            continue;
        }

        out.push(ch);
    }

    return out.trim().to_string();
}
