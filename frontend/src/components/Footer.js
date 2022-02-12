import React from "react";
import styled from "styled-components";

// Bootstrap
import Container from "react-bootstrap/Container";

const FooterContainer = styled.footer`
	height: 60px;
	width: 100%;
	background: rgba(33, 37, 41, 1);
	display: flex;
	justify-content: center;
	align-items: center;
`;

const FooterText = styled.h6`
	text-align: center;
	color: #d3d3d3;
	cursor: pointer;
	font-size: 16px;
	text-transform: uppercase;
`;

const Footer = () => {
	return (
		<FooterContainer>
			<Container>
				<FooterText>terms & conditions</FooterText>
			</Container>
		</FooterContainer>
	);
};

export default Footer;
