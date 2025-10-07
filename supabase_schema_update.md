# Supabase Schema Update

To support the new PIN feature, you need to add a PIN column to the `verified_producers` table in Supabase.

## SQL Command

```sql
ALTER TABLE verified_producers ADD COLUMN IF NOT EXISTS pin INTEGER;
```

This command will:
1. Add a new `pin` column to the `verified_producers` table
2. Use INTEGER type to store the 6-digit PIN
3. Use IF NOT EXISTS to prevent errors if the column already exists

## Alternative Approach

If you prefer to set additional constraints:

```sql
ALTER TABLE verified_producers ADD COLUMN IF NOT EXISTS pin INTEGER CHECK (pin >= 100000 AND pin <= 999999);
```

This adds a check constraint to ensure the PIN is always a 6-digit number.

## How to Execute

1. Go to your Supabase project dashboard
2. Navigate to the SQL editor
3. Run one of the above commands
4. The column will be added to your table

The Agent1 code will now be able to store and retrieve PINs for verified producers.