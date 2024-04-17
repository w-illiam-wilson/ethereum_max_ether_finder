poetry run python main.py https://magical-thrumming-needle.quiknode.pro/f43cee9d3c566de8afb1e03e948fc3dcaab7462b/ test.sqlite3 200-199

poetry run python main.py https://magical-thrumming-needle.quiknode.pro/f43cee9d3c566de8afb1e03e948fc3dcaab7462b/ test.sqlite3 18908800-18909050


SELECT
	blockNumber
FROM
	blocks
WHERE
	weiValue = (SELECT MAX(weiValue) FROM blocks);