import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import styled from "styled-components";
import { Link } from "../components/Elements";
// data
import { countries, images } from "../data";

// Bootstrap
import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";

// Custom
import { Section } from "../components/Elements";

const ImageContainer = styled.div`
	display: flex;
	justify-content: center;
	align-items: center;
`;

const CardImage = styled.img`
	max-width: 400px;
`;

const CardHeader = styled.h4`
	padding: 0.5rem 0;
	font-size: 3rem;
	color: #27ae60;
	text-align: center;
`;

const CardText = styled.h4`
	position: relative;
	padding: 0.5rem 0;
	font-size: 1.2rem;
	color: #777;
`;

const Form = styled.form``;
const FormGroup = styled.div`
	span {
		display: inline=block;
		margin-right: 10px;
		font-size: 18px;
		color: #27ae60;
	}
`;
const FormInput = styled.input`
	width: 50px;
	border: 2px solid #eee;
	border-radius: 10px;

	&:focus {
		border: 1px solid #27ae60;
	}
`;
const FormBtn = styled.button`
	background: #27ae60;
	color: #fff;
	font-size: 1.2rem;
	border: none;
	padding: 5px 15px;
	margin-top: 15px;

	&:hover {
		background: #00e360;
	}
`;

const SubText = styled.span`
	font-size: 0.9rem;
`;

const BackBtn = styled(Link)`
	text-decoration: none;
	position: absolute;
	top: 40px;
	left: 120px;
	background: #fff;
	color: #fff;
	font-size: 1.2rem;
	border: none;
	border-radius: 50%;
	padding: 10px;
	margin-top: 15px;

	.fas {
		font-size: 2.5rem;
		color: #27ae60;
	}

	&:hover {
		.fas {
			color: #00e360;
		}
	}
`;
const CountryDetail = () => {
	const { countryID } = useParams();
	const [country, setCountry] = useState(countries[countryID - 1]);

	useEffect(() => {
		setCountry(countries[countryID - 1]);
	}, [countryID]);

	const CardFormContainer = styled(Row)`
		background: #fff;
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.4);
	`;
	return (
		<>
			<Section height="md" bgImage={images.BG}></Section>

			<Section className="p-5">
				<BackBtn to="/">
					<i className="fas fa-arrow-left"></i>
				</BackBtn>
				<CardFormContainer>
					<Col md={6} className="p-5">
						<ImageContainer>
							<CardImage src={country.image} />
						</ImageContainer>
					</Col>
					<Col md={6} className="p-5">
						<CardHeader>{country.name}</CardHeader>
						<CardText>
							Lorem, ipsum dolor sit amet consectetur adipisicing
							elit. Sed harum nemo tenetur voluptate nihil esse
							voluptas quia, perferendis error suscipit animi
							optio fuga aperiam doloribus sunt ex iusto
							recusandae eveniet?
						</CardText>
						<Form>
							<FormGroup>
								<span>Current Bid:</span>
								<FormInput type="text" placeholder="0" />
							</FormGroup>
							<FormBtn>Submit</FormBtn>
						</Form>
						<CardText></CardText>
						<SubText>
							DESCLAIMER: *Lorem, ipsum dolor sit amet consectetur
							adipisicing elit.
						</SubText>
					</Col>
				</CardFormContainer>
			</Section>
		</>
	);
};

export default CountryDetail;
