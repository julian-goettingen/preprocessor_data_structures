

# das main-loop muss geändert werden, damit $A durch das dictionary von A ersetzt werden können.
# Vielleicht kann man dabei auch den target-file-stack durch ein intelligenteres producer-consumer-konzept ersetzt werden.
# Jede Zeile kann eines von diesen sein:
# einen consumer öffnen (zB #include PPDS_TARGET_DEF...)
# einen consumer schließen (zB #include PPDS_TARGET_UNDEF...)
# einen producer hinzufügen (zB #include PPDS_SOURCE...)
# einen producer benutzen und die Datenstruktur erstellen(zB PPDS_DECLARE_)
# Es können auch schon standard-consumer existieren (für python und .c boilerplate?)

class PPDSClass:
    """
    represents a DataClass as defined by the source-header;
    meaning an example instance of this would be ARR3D (not an instance of ARR3D)
    """

    def __init__(self, source_header_path):

        self.constructors =

    def make_instance(self):

class PPDSInstance:
    """
    An instance of this represents an instance of a PPDSDataClass
    meaning ann example instance would be
    """

    def __init__(self):

def handle_file(src):

    producers = {} # name -> Producer-instance

    # eine sink braucht irgendwie eine Bedingung, um getriggert zu werden und dann über alle producers zu klettern.
    # eigentlich nur das Ende des files
