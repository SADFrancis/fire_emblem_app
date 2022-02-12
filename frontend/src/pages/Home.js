import React from "react";

// Bootstrap
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
// Custom Components
import { Section, Link } from "../components/Elements";
import Card from "../components/Card";

// Data
import { images } from "../data";

const Home = ({ countries }) => {
	return (
		<>
			<Section height="md" bgImage={images.BG}></Section>
			<Section>
				<Row className="p-5">
					{countries.map((country, key) => (
						<Col md={4} key={key} className="my-3">
							<Link to={`/countries/${key + 1}`}>
								<Card img={country.image} name={country.name} />
							</Link>
						</Col>
					))}
				</Row>
			</Section>
		</>
	);
};

export default Home;
