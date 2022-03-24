import psycopg
# import psycopg_c

print(psycopg.__version__)

conn = psycopg.connect(
    autocommit=False,
    conninfo=
    'dbname=test_db user=edm_test_user password=EDM_TEST_USER host=172.16.118.110 port=5432'
)

cur = conn.cursor()

cur.execute('select count(1) from edm_test_schema.edm_test_table;')

rst = cur.fetchall()[0]

print(rst)

cur.close()
conn.close()