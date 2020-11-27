const { healthHandler } = require("./handler");

module.exports = path => {
	switch (path) {
		case "/hoover-health":
			return {
				GET: healthHandler,
				POST: healthHandler
			};
	}
};
