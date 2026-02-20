const { GoogleGenerativeAI } = require("@google/generative-ai");
const fs = require('fs');

const apiKey = process.env.GOOGLE_GENERATIVE_AI_API_KEY || process.env.GOOGLE_API_KEY;
if (!apiKey) {
    console.error("❌ No API Key! Run: export GOOGLE_GENERATIVE_AI_API_KEY='your_key'");
    process.exit(1);
}

const genAI = new GoogleGenerativeAI(apiKey);

/**
 * PIVOT: Using Gemini 3 Flash for high-quota free tier usage.
 * Flash is the engine of choice for 2026 speed/monetization.
 */
const model = genAI.getGenerativeModel({ 
    model: "gemini-3-flash-preview",
    systemInstruction: "You are the Gilded Spear. Your mission is to find revenue in CRISPR data and leads. Be aggressive, fast, and identify the top dollar lead for Joseph Purvis."
});

async function runWithRetry(prompt, retries = 3, delay = 5000) {
    for (let i = 0; i < retries; i++) {
        try {
            const result = await model.generateContent(prompt);
            return result.response.text();
        } catch (err) {
            if (err.message.includes("429") && i < retries - 1) {
                console.log(`⚠️ Rate limit hit. Waiting ${delay/1000}s... (Attempt ${i+1}/${retries})`);
                await new Promise(res => setTimeout(res, delay));
                delay *= 2; // Wait longer each time
            } else {
                throw err;
            }
        }
    }
}

async function startEngine() {
    console.log("🚀 Launching Gilded Spear (Flash Edition)...");
    
    // Check for the files you listed
    const leads = fs.existsSync('./active_leads.json') ? fs.readFileSync('./active_leads.json', 'utf8') : "No leads found.";
    const report = fs.existsSync('./Spartan_HTT_Resonance_Report_v1.csv') ? fs.readFileSync('./Spartan_HTT_Resonance_Report_v1.csv', 'utf8').slice(0, 1000) : "No report found.";
    
    const query = `
        Leads: ${leads}
        Data: ${report}
        Task: Which lead should I contact first to make money today, and what is my pitch?
    `;
    
    try {
        const strategy = await runWithRetry(query);
        console.log("\n--- STRATEGIC REVENUE REPORT ---\n");
        console.log(strategy);
        console.log("\n--------------------------------\n");
    } catch (e) {
        console.error("❌ Final Execution Error:", e.message);
        console.log("TIP: Go to AI Studio and check if you need to enable 'Pay-as-you-go' (Free tier still applies) to unlock the quota.");
    }
}

startEngine();
