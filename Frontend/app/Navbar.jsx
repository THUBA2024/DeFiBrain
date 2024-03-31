import PropTypes from 'prop-types';
import { Wallet } from "../service/near-wallet";
import {  Flex } from 'antd';
import "./custom.css";

const  Navbar = ({wallet, isSignedIn}) =>{
    const signIn = () => { wallet.signIn() }
    const signOut = () => { wallet.signOut() }
    return( 
    <Flex className="container-fluid navbar-expand-lg" style={{ justifyContent: 'end', width: '100%'}}>
      {isSignedIn
            ? <button onClick={signOut} className='customButton' style={{width: "100px"}}>Logout</button>
            : <button onClick={signIn} className='customButton'>Login</button>
      }
    </Flex>)
}

Navbar.propTypes = {
    wallet: PropTypes.instanceOf(Wallet),
    isSignedIn: PropTypes.bool.isRequired,
  };
  

export default Navbar