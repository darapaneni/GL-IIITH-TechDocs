from DBConnect import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

 #############################
class Common(Base):
    __abstract__ = True

    DocId           = Column(Integer, primary_key=True, autoincrement=True)
    DocName         = Column(String(256))
    UserId          = Column(String(256))
    IsUpload        = Column(Boolean, default=False)
    IsTrash         = Column(Boolean, default=False)
    FilePath        = Column(Text)
    Version         = Column(Integer)
    CreatedDate     = Column(DateTime)
    s_Misc1         = Column(String(1024))
    s_Misc2         = Column(String(1024))
    n_Misc1         = Column(Integer)
    n_Misc2         = Column(Integer)
    
 
    #Constructor methods to insert data into Documents table
    def __init__(self, UserId, DocName, Filepath, Datetime, Version, IsUpload, IsTrash):
        self.UserId      = UserId
        self.DocName     = DocName
        self.FilePath    = Filepath
        self.CreatedDate = Datetime
        self.Version     = Version
        self.IsUpload    = IsUpload
        self.IsTrash     = IsTrash