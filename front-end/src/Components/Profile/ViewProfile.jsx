import React from 'react'

import { useParams } from 'react-router-dom'

import './Profile.css'

import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import PortraitIcon from '@mui/icons-material/Portrait';

function ViewProfile() {

    const { userID } = useParams();

    return (
        <div id="view_profile_container">
            <div id="view_profile_top">
                <div id="view_profile_back_button">
                    <ArrowBackIosNewIcon style={{cursor: 'pointer'}} />
                </div>
            </div>
            <div id="view_profile_mid">
                <div id="view_profile_mid_left">
                    <PortraitIcon style={{fontSize: 250}}/>
                </div>
                <div id="view_profile_mid_mid">
                    <div id="view_profile_seller_name">
                        Insert Name
                    </div>
                    <div id="view_profile_seller_email">
                        Insert Email
                    </div>
                    <div id="view_profile_rating">
                        Insert Rating
                    </div>
                    <div id="view_profile_action_buttons">
                        <div id="view_profile_email_button">
                            Email
                        </div>
                        <div id="view_profile_chat_button">
                            Chat
                        </div>
                        <div id="view_profile_report_button">
                            Report
                        </div>
                    </div>
                </div>
                <div id="view_profile_mid_right">
                    Description:<br />
                </div>
            </div>
            <div id="view_profile_bot">

            </div>
        </div>
    )
}

export default ViewProfile;