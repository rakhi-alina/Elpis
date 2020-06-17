from abc import abstractmethod
from pathlib import Path
from elpis.engines.common.objects.model import Model
from elpis.engines.common.objects.fsobject import FSObject


class Transcription(FSObject):
    _config_file = "transcription.json"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = None
        self.config["model_name"] = None
        self.config["status"] = "ready"
        self.type = None
        self._exporter = None
        self.config['exporter'] = None
        self.config['has_been_transcribed'] = False

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.model = None

        self._exporter = self.config['exporter']
        if self._exporter != None:
            exporter_name = self._exporter['name']
            self.select_exporter(exporter_name)
        return self

    def link(self, model: Model):
        self.model = model
        self.config['model_name'] = model.name

    @property
    def status(self):
        return self.config['status']

    @status.setter
    def status(self, value: str):
        self.config['status'] = value
    
    @property
    def state(self):
        return {
            'name': self.config['name'],
            'hash': self.config['hash'],
            'date': self.config['date'],
            'model': self.config['model_name'],
            'has_been_transcribed': self.config['has_been_transcribed'],
            'exporter': self.config['exporter']
        }
    
    @property
    def has_been_transcribed(self):
        return self.config['has_been_transcribed']
    
    @property
    def exporter(self):
        return self._exporter

    @abstractmethod
    def transcribe(self, *args, **kwargs):
        pass

    @abstractmethod
    def text(self):
        pass

    @abstractmethod
    def elan(self):
        pass
