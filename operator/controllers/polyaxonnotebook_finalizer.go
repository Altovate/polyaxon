/*
Copyright 2019 Polyaxon, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package controllers

import (
	"context"

	corev1alpha1 "github.com/polyaxon/polyaxon-operator/api/v1alpha1"
)

func (r *PolyaxonNotebookReconciler) addFinalizer(instance *corev1alpha1.PolyaxonNotebook) error {
	instance.AddFinalizer()
	return r.Update(context.Background(), instance)
}

func (r *PolyaxonNotebookReconciler) handleFinalizer(instance *corev1alpha1.PolyaxonNotebook) error {
	if !instance.HasFinalizer() {
		return nil
	}

	if err := r.setStatus(instance); err != nil {
		return err
	}
	instance.RemoveFinalizer()
	return r.Update(context.Background(), instance)
}

func (r *PolyaxonNotebookReconciler) setStatus(instance *corev1alpha1.PolyaxonNotebook) error {
	log := r.Log

	log.Info("Notebook end", "Reconciliation", instance.GetName())

	// Add logic to send status update to experiment based on the rel_url metadata
	// rel_url := instance.Status.Metadata.owner/project/experimentId
	// if it fails just let it be
	// return r.APIClient.Experiments().setStatus(owner, project, experimentId
	return nil
}
