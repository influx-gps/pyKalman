# E2E test

To run test you simply need to run:
<br/>
`python data_sending_test.py <app_url>/kalman/<track_id>`

<br/>
* where app_url is url to running app instance and track_id could be random number
* if you won't specify an argument with url, test will try to sent data on localhost:9099
<br/>

The result of test is drown map of two trajectories - blue native and green filtered.
