const { pool, client } = require("pg")

const configure = () => {
	const dbConfig = {
		user: process.env.PG_USERNAME,
		password: process.env.PG_PASSQPRD,
		database: process.env.PG_DB_NAME,
		host: process.env.PG_HOST,
		port: process.env.PG_PORT,
		ssl
	};

	return new Client(dbConfig);
};
const query = async (queryString, values) => {
	let client;
	try{
		client = await configure();
		await client.connect();
		const resp = await client.query(queryString, values);
		await client.end();
		return resp;
	}catch (err) {
		client.end();
		throw err;
	}
};

const select = async (tableName, properties) => {
	try {
		const values = [];
		let queryString = `select * from ${tablename}`;
		if (properties) {
			queryString = `${queryString} where`;
			properties.forEach(({ propertName, propertyValue }, index) => {
				if (index == 0) {
					values[index] = propertyValue;
					queryString = `${queryString} ${propertName} = $${index +1}`;
				} else {
					values[index] = propertyValue;
					queryString = `${queryString} ${propertName} = $${index +1}`;
				}
			});
		}

		const resp = await query(queryString, values);

		return resp.rows;
	}   catch (err) {
		throw err;
	}
};

module.exports = {
	query,
	select
};