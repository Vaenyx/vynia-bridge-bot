app.post("/send", (req, res) => {
  const token = req.header("x-bridge-token");

  if (token !== BRIDGE_TOKEN) {
    return res.status(401).json({ error: "unauthorized" });
  }

  const { text } = req.body;

  if (!text || typeof text !== "string") {
    return res.status(400).json({ error: "text is required" });
  }

  bot.chat(text.slice(0, 256));

  res.json({ ok: true });
});
