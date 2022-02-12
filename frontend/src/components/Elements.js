import styled from "styled-components";
import { Link as RLink } from "react-router-dom";
// Bootstrap
import Container from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";

const sectionHeight = {
	full: "100vh",
	md: "50vh",
};
const SectionStyle = styled.section`
	height: ${(props) => (props.height ? sectionHeight[props.height] : "")};
	background: linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.2)),
		url(${(props) => props.bgImage});
	background-position: center;
	background-repeat: no-repeat;
	background-size: cover;
	position: relative;
`;

export const Section = (props) => {
	return (
		<SectionStyle
			className={props.className}
			height={props.height}
			bgImage={props.bgImage}
		>
			<Container>{props.children}</Container>
		</SectionStyle>
	);
};

export const Link = styled(RLink)`
	text-decoration: none;

	&:hover {
		color: none;
	}
`;
