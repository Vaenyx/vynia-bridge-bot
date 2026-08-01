pub mod client;
pub mod commands;
pub mod formatting;

use crate::apis::urchin::UrchinApi;

pub struct Data {
    pub urchin: UrchinApi,
}

pub type Error = crate::error::Error;
pub type Context<'a> = poise::Context<'a, Data, Error>;
