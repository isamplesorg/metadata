 * [domain_of](/biolinkml/docs/domain_of.html)    0..many    Description: the class(es) that reference the slot in a "slots" or "slot_usage" context.  range: [ClassDefinition](/biolinkml/docs/ClassDefinition.html)  

 * [identifier](/biolinkml/docs/identifier.html)  OPT  Description: True means that the key slot(s) uniquely identify the container. There can be at most one identifier or key per container. range: [Boolean](/biolinkml/docs/types/Boolean.html)  


 * [ifabsent](/biolinkml/docs/ifabsent.html)  OPT   Description: function that provides a default value for the slot.  Possible values for this slot are defined in biolink.utils.ifabsent_functions.default_library:   * [Tt]rue -- boolean True   * [Ff]alse -- boolean False   * int(value) -- integer value   * str(value) -- string value   * default_range -- schema default range   * bnode -- blank node identifier   * slot_uri -- URI for the slot   * class_curie -- CURIE for the containing class   * class_uri -- URI for the containing class.  range: [String](/biolinkml/docs/types/String.html)  

 *  [inherited](/biolinkml/docs/inherited.html)  OPT   * Description: true means that the *value* of a slot is inherited by subclasses.  Range: [Boolean](/biolinkml/docs/types/Boolean.html)  

 *  [inlined](/biolinkml/docs/inlined.html)  OPT   * Description: True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere. .  Range: [Boolean](/biolinkml/docs/types/Boolean.html)
 
 * [inlined_as_list](/biolinkml/docs/inlined_as_list.html)    OPT   * Description: True means that an inlined slot is represented as a list of /range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance..  Range: [Boolean](/biolinkml/docs/types/Boolean.html)  
  
 *  [inverse](/biolinkml/docs/inverse.html)    OPT   * Description: indicates that any instance of d s r implies that there is also an instance of r s' d. .  Range: [SlotDefinition](/biolinkml/docs/SlotDefinition.html)  
 
 *  [is_class_field](/biolinkml/docs/is_class_field.html)    OPT   * Description: indicates that any instance, i,  the domain of this slot will include an assert of i s range. .  Range: [Boolean](/biolinkml/docs/types/Boolean.html)  
 
 *  [is_usage_slot](/biolinkml/docs/is_usage_slot.html)    OPT   * Description: True means that this slot was defined in a slot_usage situation. .  Range: [Boolean](/biolinkml/docs/types/Boolean.html)  
  
 *  [key](/biolinkml/docs/key.html)    OPT   * Description: True means that the key slot(s) uniquely identify the container. In future releases, it will be possible for there to be compound keys, where several slots combine to produce a unique identifier. .  Range: [Boolean](/biolinkml/docs/types/Boolean.html)  
 
 *  [maximum_value](/biolinkml/docs/maximum_value.html)    OPT   * Description: for slots with ranges of type number, the value must be equal to or lowe than this. .  Range: [Integer](/biolinkml/docs/types/Integer.html)  
 
 *  [minimum_value](/biolinkml/docs/minimum_value.html)    OPT   * Description: for slots with ranges of type number, the value must be equal to or higher than this. .  Range: [Integer](/biolinkml/docs/types/Integer.html)  
 
 *  [multivalued](/biolinkml/docs/multivalued.html)    OPT   * Description: true means that slot can have more than one value. .  Range: [Boolean](/biolinkml/docs/types/Boolean.html) .   
 *  [owner](/biolinkml/docs/owner.html)    OPT   * Description: the "owner" of the slot. It is the class if it appears in the slots list, otherwise the declaring slot.  Range: [Definition](/biolinkml/docs/Definition.html)  
 
 *  [pattern](/biolinkml/docs/pattern.html)    OPT   * Description: the string value of the slot must conform to this regular expression.  Range: [String](/biolinkml/docs/types/String.html)  
 
 *  [range](/biolinkml/docs/range.html)    OPT   * Description: defines the type of the object of the slot.  Given the following slot definition   S1:domain: C1; range:  C2;  the declaration X: S1: Y implicitly asserts Y is an instance of C2 .  Range: [Element](/biolinkml/docs/Element.html)  
 
*  [readonly](/biolinkml/docs/readonly.html)    OPT   * Description: If present, slot is read only.  Text explains why.  Range: [String](/biolinkml/docs/types/String.html)  
 
 *  [required](/biolinkml/docs/required.html)    OPT   * Description: true means that the slot must be present in the loaded definition.  Range: [Boolean](/biolinkml/docs/types/Boolean.html)  
 
 *  [role](/biolinkml/docs/role.html)    OPT   * Description: the role played by the slot range.  Range: [String](/biolinkml/docs/types/String.html)  
 
 *  [singular_name](/biolinkml/docs/singular_name.html)    OPT   * Description: a name that is used in the singular form.  Range: [String](/biolinkml/docs/types/String.html)  
 
 *  [slot_definition➞apply_to](/biolinkml/docs/slot_definition_apply_to.html)    0..*    Range: [SlotDefinition](/biolinkml/docs/SlotDefinition.html)  

 * [slot_definition➞is_a](/biolinkml/docs/slot_definition_is_a.html)    OPT    Range: [SlotDefinition](/biolinkml/docs/SlotDefinition.html)  
 
 *  [slot_definition➞mixins](/biolinkml/docs/slot_definition_mixins.html)    0..*    Range: [SlotDefinition](/biolinkml/docs/SlotDefinition.html)  

 * [slot_uri](/biolinkml/docs/slot_uri.html)    OPT   * Description: predicate of this slot for semantic web application.  Range: [Uriorcurie](/biolinkml/docs/types/Uriorcurie.html)  
 
 *  [string_serialization](/biolinkml/docs/string_serialization.html)    OPT   * Description: Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots. We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion. Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objects For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm.  Range: [String](/biolinkml/docs/types/String.html)  
 
 *  [subproperty_of](/biolinkml/docs/subproperty_of.html)    OPT   * Description: Ontology property which this slot is a subproperty of.   .  Range: [SlotDefinition](/biolinkml/docs/SlotDefinition.html)  
 
 *  [symmetric](/biolinkml/docs/symmetric.html)    OPT   * Description: True means that any instance of  d s r implies that there is also an instance of r s d.  Range: [Boolean](/biolinkml/docs/types/Boolean.html)  
  
 *  [usage_slot_name](/biolinkml/docs/usage_slot_name.html)    OPT   * Description: The name of the slot referenced in the slot_usage.  Range: [String](/biolinkml/docs/types/String.html)