/**
 * Migration script to migrate projects from JSON to Parse Objects
 * 
 * Usage:
 * 1. Install dependencies: npm install parse
 * 2. Set environment variables:
 *    - PARSE_APPLICATION_ID
 *    - PARSE_MASTER_KEY
 *    - PARSE_SERVER_URL (default: https://parseapi.back4app.com)
 * 3. Run: node migrate_to_parse.js
 */

const Parse = require("parse/node");
const fs = require("fs");
const path = require("path");

// Initialize Parse
const APPLICATION_ID = process.env.PARSE_APPLICATION_ID || "RHgQk1lCAS2mybB5ZLa7OPaMsFv3g2mpFECwQ7RC";
const MASTER_KEY = process.env.PARSE_MASTER_KEY || "FeZyWrL0kJvBXDS4jDdnTPoymFyuLGcwjQztjDTJ";
const SERVER_URL = process.env.PARSE_SERVER_URL || "https://parseapi.back4app.com";

Parse.initialize(APPLICATION_ID, null, MASTER_KEY);
Parse.serverURL = SERVER_URL;
Parse.masterKey = MASTER_KEY;

async function migrateProjects() {
  console.log("Starting migration...");
  
  // Read projects.json
  const projectsPath = path.join(__dirname, "app", "db", "projects.json");
  if (!fs.existsSync(projectsPath)) {
    console.error("projects.json not found at:", projectsPath);
    process.exit(1);
  }

  const projectsData = JSON.parse(fs.readFileSync(projectsPath, "utf8"));
  console.log(`Found ${Object.keys(projectsData).length} projects to migrate`);

  const Project = Parse.Object.extend("Project");
  let migrated = 0;
  let errors = 0;

  for (const [apiKey, projectData] of Object.entries(projectsData)) {
    try {
      // Check if project already exists
      const query = new Parse.Query(Project);
      query.equalTo("api_key", apiKey);
      const existing = await query.first({ useMasterKey: true });

      if (existing) {
        console.log(`Project with API key ${apiKey} already exists, skipping...`);
        continue;
      }

      // Create new project
      const project = new Project();
      project.set("project_id", projectData.project_id);
      project.set("api_key", apiKey);
      project.set("company_name", projectData.company_name);
      project.set("site_name", projectData.site_name);
      project.set("website_url", projectData.website_url);
      project.set("company_size", projectData.company_size || null);
      project.set("industry", projectData.industry || null);
      project.set("contact_email", projectData.contact_email || null);
      project.set("is_active", projectData.is_active !== false);
      
      // Parse date
      if (projectData.created_at) {
        const createdAt = typeof projectData.created_at === "string" 
          ? new Date(projectData.created_at) 
          : projectData.created_at;
        project.set("created_at", createdAt);
      } else {
        project.set("created_at", new Date());
      }

      // Set API keys if they exist
      if (projectData.gemini_key) {
        project.set("gemini_key", projectData.gemini_key);
      }
      if (projectData.groq_key) {
        project.set("groq_key", projectData.groq_key);
      }

      await project.save(null, { useMasterKey: true });
      console.log(`✓ Migrated project: ${projectData.company_name} (${apiKey})`);
      migrated++;

    } catch (error) {
      console.error(`✗ Error migrating project ${apiKey}:`, error.message);
      errors++;
    }
  }

  console.log("\nMigration complete!");
  console.log(`Migrated: ${migrated}`);
  console.log(`Errors: ${errors}`);
}

// Run migration
migrateProjects()
  .then(() => {
    console.log("Done!");
    process.exit(0);
  })
  .catch((error) => {
    console.error("Migration failed:", error);
    process.exit(1);
  });


