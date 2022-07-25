### Organization of the Schema
The schema is organized in a hierarchical fashion similar to many introductory object oriented projects. In the `models/localize/common` folder, there are many objects which are shared across different events to minimize schema text duplication. Additionally, there is a field, `core_event.yaml` which is the base event that all events inherit from. Each folder besides `common` represents an `event_category`. In each event category folder, there is a file that matches the folder name. For example, in the `property_event` folder, there is a file named `property_event.yaml`. This file represents the category itself and all events of the property event inherit from this file. All fields in the category file are inherited by each property_event category event. If you wish to change something for all property_events, you would edit or update this file. All other files inside of the folder represent the specific events themselves.
 
It is important to understand that the structure of the events informs the structure of the Redshift tables. Each event contains various fields that are generally shared across all other events. These fields become columns in Redshift such as a `browser__page_type` column. Inside of every terminal YAML file corresponding to an event action, there is an optional `event` object that can be placed. This is where all the contextual data related to the event must be stored. This event object becomes a JSON column inside of Redshift.
 
Additionally, the Redshift columns are built by recursively scanning all of the YAML (technically JSON during the script) and creating columns that are delimited by `__` to indicate the hierarchical structure of the YAML. This example is shown above with the browser and the page type field. Because of the recursive structure, it is important to not reuse names across the hierarchies as this can potentially cause conflicts in Redshift.
 
### Working with the Schema
The schema is written in [YAML](https://yaml.org/). YAML is a super set of JSON and contains more features and power than JSON while also being, easier to read. Our schema uses a few specific attributes that are important to understand when modifying or creating new schema.
 
- allOf: All categories and events start with this. This ensures proper inheritance behavior in the event.
- $ref: This is used to refer to other YAML both for inheritance and encapsulation. This is the classic "is a" and "contains a" concept in object oriented programming. A `.` is a reference to the current relative directory and a `..` is a reference to the parent directory of the current relative directory.
- description: Used to define anything for better understanding by analysts and front end developers.
- properties: The actual fields that make up a specific object, category, or event.
- enum: A collection of objects which are defined in advance. This is used when you wish to enforce strict validation of what you expect. We commonly use this for string types but you can use this for other types as well.
- required: Specifies which fields are required for an object to be considered valid. This is critical to understand in that placing a field in the required object can break backwards compatibility of the schema with the front end.
- type: Specifies the type of data. This is important as the type also maps to Redshift. An integer maps to a Redshift `INTEGER` and a number maps to a Redshift `DOUBLE PRECISION`.
- additionalProperties: A boolean value which states if the API will accept additional properties not defined in the schema. Always specify this to `false` if possible so that our data validation is as strict as possible.
- maxLength: Used to define the maxLength of strings. This is very important for all fields outside of the event object to build the Redshift columns and to validate the strings the EventAPI receives.
- title: Used to define the object. This is only useful for the machine generated documentation.
 
By perusing the documentation, one should understand the patterns that emerge while editing and creating YAML.
 
There are some important considerations to take when updating the event schema. **Every string type object must have a maxLength for Redshift purposes.** This maxLength is mapped to a VARCHAR column.
