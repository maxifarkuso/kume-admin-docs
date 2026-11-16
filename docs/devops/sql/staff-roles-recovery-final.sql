SELECT 'ok'
WHERE EXISTS (
  SELECT 1 FROM information_schema.columns
  WHERE table_schema = 'public' AND table_name = 'expense'
    AND column_name = 'due_date' AND data_type = 'date'
    AND is_nullable = 'YES' AND column_default IS NULL
)
AND EXISTS (
  SELECT 1 FROM pg_catalog.pg_index i
  WHERE i.indexrelid = to_regclass('public.expense_due_date_idx')
    AND i.indrelid = 'public.expense'::regclass
    AND i.indisvalid AND i.indisready AND i.indnatts = 1
    AND i.indexprs IS NULL AND i.indpred IS NULL
    AND i.indkey[0] = (
      SELECT attnum FROM pg_catalog.pg_attribute
      WHERE attrelid = 'public.expense'::regclass AND attname = 'due_date'
        AND NOT attisdropped
    )
)
AND (
  SELECT count(*) FROM public._prisma_migrations
  WHERE migration_name = '202611160001_expense_due_date'
    AND checksum = 'e8f0560188a963c09a85ede6704b20fce7064c12c908b6e43902a8fe8b082361'
    AND finished_at IS NOT NULL AND rolled_back_at IS NULL
) = 1
AND (
  SELECT array_agg(m[1] ORDER BY m[1] COLLATE "C")
  FROM pg_catalog.pg_constraint c
  CROSS JOIN LATERAL regexp_matches(
    pg_get_constraintdef(c.oid), '''([^'']+)''', 'g'
  ) AS m
  WHERE c.conrelid = 'public.staff_member'::regclass
    AND c.conname = 'staff_member_role_check'
    AND c.contype = 'c' AND c.convalidated
) = ARRAY['classroomAssistant', 'classroomLead', 'cleaningAssistant',
  'director', 'teacher', 'workshopInstructor']::text[]
AND (
  SELECT count(*) FROM public._prisma_migrations
  WHERE migration_name = '202611160002_staff_roles'
    AND finished_at IS NOT NULL AND rolled_back_at IS NULL
    AND checksum = '3042743837cddb19833aa4a378982270a839e7eda36365fb116d45e0abc2e0c1'
) = 1
AND NOT EXISTS (
  SELECT 1 FROM public._prisma_migrations
  WHERE (finished_at IS NULL AND rolled_back_at IS NULL)
     OR (finished_at IS NOT NULL AND rolled_back_at IS NOT NULL)
);
