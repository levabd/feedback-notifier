# Structure

## Table «feedback_messages»

   Field            |  Type  | Description
------------------: | :----- | :--------------------------------------------------------------------------------------------------------
**os**              | STRING | `ios` or `android`
**id**              | STRING | Id of review.
**author**          | STRING | The name of the user who wrote the review.
**comment**         | STRING | The content of the comment, i.e. review body.
**updated_at**      | INT    | The last time at which this comment was updated in seconds. iOS in GMT Timezone, Android in customers Timezone 
**rating**          | INT    | The star rating associated with the review, from 1 to 5.
**device**          | STRING | Codename for the reviewer's device, e.g. klte, flounder.
**os_version**      | INT    | Integer Android SDK version of the user's device at the time the review was written, e.g. 23 is Marshmallow.
**app_version**     | STRING | String version name of the app as installed at the time the review was written.
**device_metadata** | STRING | JSON object with full metadata of device
