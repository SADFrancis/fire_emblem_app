import React from "react";
import styled from "styled-components";

const CardImage = styled.img`
	width: 300px;
	height: 300px;
`;

const CardHeader = styled.h4`
	padding: 0.5rem 0;
	font-size: 2rem;
	color: #444;
`;

const CardContainer = styled.div`
	display: flex;
	justify-content: center;
	align-items: center;
	flex-direction: column;
	width: 100%;
	background: #fff;
	box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.4);
	transition: 0.3s;
	padding: 15px;

	&:hover {
		box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.6);
	}

	&:hover ${CardImage} {
		transform: scale(0.9);
	}

	&:hover ${CardHeader} {
		color: #27ae60;
	}
`;

const Card = ({ img, name }) => {
	return (
		<>
			<CardContainer>
				<CardImage src={img} />
				<CardHeader>{name}</CardHeader>
			</CardContainer>
		</>
	);
};

export default Card;
