import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import axios from "axios";

// Custom Components
import Home from "./pages/Home";
import Footer from "./components/Footer";
import CountryDetail from "./pages/CountryDetail";

const App = () => {
	const [isLoading, setIsLoading] = useState(false);
	const [countries, setCountries] = useState([]);

	useEffect(() => {
		axios
			.get("http://127.0.0.1:8000/countries/")
			.then(function (response) {
				// handle success
				setCountries(response.data);
			})
			.catch(function (error) {
				// handle error
				console.log(error);
			})
			.then(function () {
				// always executed
			});
	}, []);

	return (
		<Router>
			{isLoading ? (
				<h1>Loading...</h1>
			) : (
				<>
					<Routes>
						<Route
							path="/"
							element={<Home countries={countries} />}
						/>
						<Route
							exact
							path="/countries/:countryID"
							element={<CountryDetail />}
						/>
					</Routes>
					<Footer />
				</>
			)}
		</Router>
	);
};

export default App;
