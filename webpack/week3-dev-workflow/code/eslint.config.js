const tseslint = require("@typescript-eslint/eslint-plugin");
const tsParser = require("@typescript-eslint/parser");
const eslintConfigPrettier = require("eslint-config-prettier");

module.exports = [
  {
    files: ["src/**/*.{ts,tsx,js}"],
    languageOptions: {
      parser: tsParser,
      ecmaVersion: "latest",
      sourceType: "module"
    },
    plugins: {
      "@typescript-eslint": tseslint
    },
    rules: {
      ...tseslint.configs.recommended.rules,
      "no-console": "off"
    }
  },
  eslintConfigPrettier
];
