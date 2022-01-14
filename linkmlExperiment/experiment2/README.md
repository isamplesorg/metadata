This experiment addressed a number of requirements surfaced since the last experiment. In particular, we are not validating json data against the yaml schema. And instead of employing linkml:PermissibleValue model (https://linkml.io/linkml-model/docs/PermissibleValue/) we prefer a simpler representation. LinkML version used 1.1.15. 

**Edits needed in our iSamplesSchemaBasic0.3.yaml (= 0.3.yaml) to generate 0.3.hong.edited.yaml**
1. Changed Name: to PhysicalSampleRecord
2. Added “type” and “$schema” slots in PysicalSampleRecord and define them in Slots
3. Added “type” to each of the classes
4. Enums:  replaced phrase strings with CURIEs of the terms, terms updated according to the vocab ttl files on github Jan 14, 2022
5. Added inlined_as_list:true to all properties with nested properties
6. Updated URIs for CVs  to use w3id URIs
7. Added "linkml": "https://w3id.org/linkml/" and imports:   - linkml:types, and removed our type definitions.


**Json schema 0.3.linkml.schema.json was generated, no manual edit needed. [when validate files, may need to set "additionalProperties": false].** Command used: 

```gen-json-schema -t PhysicalSampleRecord 0.3.hong.edited.yaml > 0.3.linkml.schema.json
```
**Next, generate Jsonld context, context.jsonld, from 0.3.hong.edited.yaml**, using

```
gen-jsonld-context 0.3.hong.edited.yaml > context.jsonld
```

And edit context.jsonld to create context.edited.jsonld by 
1. Replace @context{} block with "@type": "@vocab“ for the three CVs
2. Add  "type": "@type“
3. If needed, add "@base": “http://resource.isamples.org/schema/”


**Edits to Json file example Car2PIRE_0334.json to generate Car2PIRE_0334.edited.json**
1. @id => id; 
2. Add “type” for the 5 classes (e.g. "type": "isam:SamplingEvent“ for “producedBy”) and add  "type": "isam:PhysicalSampleRecord“ for the root.
3. Make curation/responsibility array ["curator:No Voucher"]
4. Use CURIE for CV terms, e.g.,  "hasMaterialCategory": ["mat:anthropogenicmaterial“]

**Lastly combine context.edited.jsonld with Car2PIRE_0334.edited.json to create Car2PIRE_0334.jsonld.** Test the correctness of Car2PIRE_0334.edited.json at https://json-ld.org/playground/. In the deployment, refer to the external context file, e.g., 

```
"@context": "https://resources.isamples.org/schema/context.edited.jsonld",
```

